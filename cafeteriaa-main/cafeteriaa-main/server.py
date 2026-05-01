from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
import uuid
from datetime import datetime, timezone
from supabase import create_client, Client
from twilio.rest import Client as TwilioClient

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Supabase connection
url: str = os.environ.get("SUPABASE_URL", "")
key: str = os.environ.get("SUPABASE_KEY", "")

if not url or not key:
    logger.error("Missing SUPABASE_URL or SUPABASE_KEY in environment variables.")

supabase: Client = create_client(url, key)

# Twilio connection
twilio_account_sid = os.environ.get("TWILIO_ACCOUNT_SID", "")
twilio_auth_token = os.environ.get("TWILIO_AUTH_TOKEN", "")
twilio_msg_svc_sid = os.environ.get("TWILIO_MESSAGING_SERVICE_SID", "")
owner_phone = os.environ.get("RESTAURANT_OWNER_NUMBER", "")

twilio_client = None
if twilio_account_sid and twilio_auth_token:
    try:
        twilio_client = TwilioClient(twilio_account_sid, twilio_auth_token)
    except Exception as e:
        logger.error(f"Failed to initialize Twilio: {e}")

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")


# ==================== MODELS ====================

class Category(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    image_url: str
    order: int = 0

class CategoryCreate(BaseModel):
    name: str
    image_url: str
    order: int = 0

class Dish(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    price: float
    category: str
    image_url: str
    is_popular: bool = False

class DishCreate(BaseModel):
    name: str
    description: str
    price: float
    category: str
    image_url: str
    is_popular: bool = False

class CartItem(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    session_id: str
    dish_id: str
    dish_name: str
    dish_price: float
    dish_image: str
    quantity: int = 1

class CartItemCreate(BaseModel):
    session_id: str
    dish_id: str

class CartItemUpdate(BaseModel):
    session_id: str
    dish_id: str
    quantity: int

class OrderItem(BaseModel):
    dish_id: str
    dish_name: str
    dish_price: float
    quantity: int

class Order(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    order_number: str
    session_id: str
    table_number: int
    items: List[OrderItem]
    total: float
    status: str = "pending"
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class OrderCreate(BaseModel):
    session_id: str
    table_number: int
    items: List[OrderItem]
    total: float

class Notification(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    order_id: str
    order_number: str
    table_number: int
    message: str
    read: bool = False
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class NotificationCreate(BaseModel):
    order_id: str
    order_number: str
    table_number: int
    message: str


# ==================== CATEGORY ROUTES ====================

@api_router.get("/categories", response_model=List[Category])
def get_categories():
    response = supabase.table("categories").select("*").order("order").execute()
    return response.data

@api_router.post("/categories", response_model=Category)
def create_category(category: CategoryCreate):
    cat_obj = Category(**category.model_dump())
    data = cat_obj.model_dump()
    supabase.table("categories").insert(data).execute()
    return cat_obj


# ==================== DISH ROUTES ====================

@api_router.get("/dishes", response_model=List[Dish])
def get_dishes(category: Optional[str] = None):
    query = supabase.table("dishes").select("*")
    if category:
        query = query.eq("category", category)
    response = query.execute()
    return response.data

@api_router.get("/dishes/popular", response_model=List[Dish])
def get_popular_dishes():
    response = supabase.table("dishes").select("*").eq("is_popular", True).execute()
    return response.data

@api_router.post("/dishes", response_model=Dish)
def create_dish(dish: DishCreate):
    dish_obj = Dish(**dish.model_dump())
    data = dish_obj.model_dump()
    supabase.table("dishes").insert(data).execute()
    return dish_obj


# ==================== CART ROUTES ====================

@api_router.get("/cart/{session_id}", response_model=List[CartItem])
def get_cart(session_id: str):
    response = supabase.table("cart").select("*").eq("session_id", session_id).execute()
    return response.data

@api_router.post("/cart/add", response_model=CartItem)
def add_to_cart(item: CartItemCreate):
    # Check if item already exists in cart
    response = supabase.table("cart").select("*").eq("session_id", item.session_id).eq("dish_id", item.dish_id).execute()
    existing = response.data
    
    if existing:
        existing_item = existing[0]
        new_quantity = existing_item["quantity"] + 1
        update_res = supabase.table("cart").update({"quantity": new_quantity}).eq("id", existing_item["id"]).execute()
        return update_res.data[0]
    
    # Get dish details
    dish_res = supabase.table("dishes").select("*").eq("id", item.dish_id).execute()
    if not dish_res.data:
        raise HTTPException(status_code=404, detail="Dish not found")
    dish = dish_res.data[0]
    
    cart_item = CartItem(
        session_id=item.session_id,
        dish_id=item.dish_id,
        dish_name=dish["name"],
        dish_price=dish["price"],
        dish_image=dish["image_url"],
        quantity=1
    )
    
    insert_res = supabase.table("cart").insert(cart_item.model_dump()).execute()
    return insert_res.data[0]

@api_router.put("/cart/update")
def update_cart_item(item: CartItemUpdate):
    if item.quantity <= 0:
        supabase.table("cart").delete().eq("session_id", item.session_id).eq("dish_id", item.dish_id).execute()
        return {"message": "Item removed from cart"}
    
    update_res = supabase.table("cart").update({"quantity": item.quantity}).eq("session_id", item.session_id).eq("dish_id", item.dish_id).execute()
    if not update_res.data:
        raise HTTPException(status_code=404, detail="Cart item not found")
    
    return {"message": "Cart updated successfully"}

@api_router.delete("/cart/remove/{session_id}/{dish_id}")
def remove_from_cart(session_id: str, dish_id: str):
    delete_res = supabase.table("cart").delete().eq("session_id", session_id).eq("dish_id", dish_id).execute()
    if not delete_res.data:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return {"message": "Item removed from cart"}

@api_router.delete("/cart/clear/{session_id}")
def clear_cart(session_id: str):
    supabase.table("cart").delete().eq("session_id", session_id).execute()
    return {"message": "Cart cleared"}


# ==================== ORDER ROUTES ====================

@api_router.post("/orders", response_model=Order)
def create_order(order: OrderCreate):
    count_res = supabase.table("orders").select("id", count="exact").execute()
    order_count = count_res.count if count_res.count is not None else 0
    order_number = f"ORD{order_count + 1:05d}"
    
    order_obj = Order(
        order_number=order_number,
        session_id=order.session_id,
        table_number=order.table_number,
        items=order.items,
        total=order.total
    )
    
    doc = order_obj.model_dump()
    doc['timestamp'] = doc['timestamp'].isoformat()
    doc['items'] = [i.model_dump() for i in order.items]
    supabase.table("orders").insert(doc).execute()
    
    # Create notification
    notification = Notification(
        order_id=order_obj.id,
        order_number=order_number,
        table_number=order.table_number,
        message=f"An order is placed from table {order.table_number}."
    )
    
    notif_doc = notification.model_dump()
    notif_doc['timestamp'] = notif_doc['timestamp'].isoformat()
    supabase.table("notifications").insert(notif_doc).execute()
    
    # Clear cart
    supabase.table("cart").delete().eq("session_id", order.session_id).execute()
    
    # Send SMS notification
    if twilio_client and twilio_msg_svc_sid and owner_phone:
        try:
            sms_body = f"New Order! #{order_number} from Table {order.table_number}. Total: ₹{order.total}. Items: "
            items_str = ", ".join([f"{i.quantity}x {i.dish_name}" for i in order.items])
            sms_body += items_str
            
            message = twilio_client.messages.create(
                messaging_service_sid=twilio_msg_svc_sid,
                body=sms_body,
                to=owner_phone
            )
            logger.info(f"SMS sent successfully: {message.sid}")
        except Exception as e:
            logger.error(f"Failed to send SMS: {e}")
    
    return order_obj

@api_router.get("/orders/history/{session_id}", response_model=List[Order])
def get_order_history(session_id: str):
    response = supabase.table("orders").select("*").eq("session_id", session_id).order("timestamp", desc=True).execute()
    orders = response.data
    for o in orders:
        if isinstance(o.get('timestamp'), str):
            o['timestamp'] = datetime.fromisoformat(o['timestamp'])
    return orders

@api_router.get("/orders/{order_id}", response_model=Order)
def get_order(order_id: str):
    response = supabase.table("orders").select("*").eq("id", order_id).execute()
    
    if not response.data:
        raise HTTPException(status_code=404, detail="Order not found")
        
    order = response.data[0]
    if isinstance(order.get('timestamp'), str):
        order['timestamp'] = datetime.fromisoformat(order['timestamp'])
    
    return Order(**order)


# ==================== NOTIFICATION ROUTES ====================

@api_router.get("/notifications", response_model=List[Notification])
def get_notifications():
    response = supabase.table("notifications").select("*").order("timestamp", desc=True).execute()
    notifs = response.data
    for n in notifs:
        if isinstance(n.get('timestamp'), str):
            n['timestamp'] = datetime.fromisoformat(n['timestamp'])
    return notifs

@api_router.put("/notifications/{notification_id}/read")
def mark_notification_read(notification_id: str):
    update_res = supabase.table("notifications").update({"read": True}).eq("id", notification_id).execute()
    
    if not update_res.data:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    return {"message": "Notification marked as read"}

@api_router.get("/notifications/unread/count")
def get_unread_count():
    count_res = supabase.table("notifications").select("id", count="exact").eq("read", False).execute()
    return {"count": count_res.count if count_res.count is not None else 0}


# ==================== ROOT ROUTE ====================

@api_router.get("/")
def root():
    return {"message": "Cafetaria API is running"}


# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)
