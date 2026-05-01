import os
from dotenv import load_dotenv
from pathlib import Path
from supabase import create_client, Client

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

url: str = os.environ.get("SUPABASE_URL", "")
key: str = os.environ.get("SUPABASE_KEY", "")

if not url or not key:
    print("Error: Missing SUPABASE_URL or SUPABASE_KEY in .env")
    exit(1)

supabase: Client = create_client(url, key)

def seed_database():
    print("Clearing existing data...")
    # Using delete() with neq to empty tables
    try:
        supabase.table("cart").delete().neq("id", "dummy").execute()
        supabase.table("notifications").delete().neq("id", "dummy").execute()
        supabase.table("orders").delete().neq("id", "dummy").execute()
        supabase.table("dishes").delete().neq("id", "dummy").execute()
        supabase.table("categories").delete().neq("id", "dummy").execute()
    except Exception as e:
        print(f"Warning during clear: {e}")
    
    print("Seeding Categories...")
    categories = [
        {
            "id": "cat_coffee",
            "name": "Coffee",
            "image_url": "https://images.unsplash.com/photo-1762657440603-2afa5580eaf8?auto=format&fit=crop&w=800&q=80",
            "order": 1
        },
        {
            "id": "cat_tea",
            "name": "Tea",
            "image_url": "https://images.unsplash.com/photo-1701933810995-3331d9ff463b?auto=format&fit=crop&w=800&q=80",
            "order": 2
        },
        {
            "id": "cat_sandwich",
            "name": "Sandwich",
            "image_url": "https://images.unsplash.com/photo-1717250180255-5509e931bded?auto=format&fit=crop&w=800&q=80",
            "order": 3
        },
        {
            "id": "cat_cookies",
            "name": "Cookies",
            "image_url": "https://images.unsplash.com/photo-1613563628001-aac5a5307153?auto=format&fit=crop&w=800&q=80",
            "order": 4
        },
        {
            "id": "cat_pizza",
            "name": "Pizza",
            "image_url": "https://images.unsplash.com/photo-1767065604070-574bb62ce4fc?auto=format&fit=crop&w=800&q=80",
            "order": 5
        },
        {
            "id": "cat_burger",
            "name": "Burger",
            "image_url": "https://images.unsplash.com/photo-1632898657999-ae6920976661?auto=format&fit=crop&w=800&q=80",
            "order": 6
        }
    ]
    
    for cat in categories:
        supabase.table("categories").insert(cat).execute()
    print("Categories seeded")
    
    print("Seeding Dishes...")
    dishes = [
        # Coffee
        {
            "id": "dish_espresso",
            "name": "Espresso",
            "description": "Rich and bold single shot espresso",
            "price": 50,
            "category": "Coffee",
            "image_url": "https://images.unsplash.com/photo-1510591509098-f4fdc6d0ff04?auto=format&fit=crop&w=800&q=80",
            "is_popular": True
        },
        {
            "id": "dish_cappuccino",
            "name": "Cappuccino",
            "description": "Classic Italian coffee with steamed milk foam",
            "price": 50,
            "category": "Coffee",
            "image_url": "https://images.unsplash.com/photo-1572442388796-11668a67e53d?auto=format&fit=crop&w=800&q=80",
            "is_popular": True
        },
        {
            "id": "dish_latte",
            "name": "Latte",
            "description": "Smooth coffee with steamed milk",
            "price": 50,
            "category": "Coffee",
            "image_url": "https://images.unsplash.com/photo-1541167760496-1628856ab772?auto=format&fit=crop&w=800&q=80",
            "is_popular": False
        },
        {
            "id": "dish_americano",
            "name": "Americano",
            "description": "Espresso with hot water",
            "price": 50,
            "category": "Coffee",
            "image_url": "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?auto=format&fit=crop&w=800&q=80",
            "is_popular": False
        },
        
        # Tea
        {
            "id": "dish_masala_chai",
            "name": "Masala Chai",
            "description": "Traditional Indian spiced tea",
            "price": 20,
            "category": "Tea",
            "image_url": "https://images.unsplash.com/photo-1597318181275-c0f61c36f1bc?auto=format&fit=crop&w=800&q=80",
            "is_popular": False
        },
        {
            "id": "dish_green_tea",
            "name": "Green Tea",
            "description": "Refreshing and healthy green tea",
            "price": 20,
            "category": "Tea",
            "image_url": "https://images.unsplash.com/photo-1627435601361-ec25f5b1d0e5?auto=format&fit=crop&w=800&q=80",
            "is_popular": False
        },
        {
            "id": "dish_lemon_tea",
            "name": "Lemon Tea",
            "description": "Refreshing tea with a zesty lemon twist",
            "price": 20,
            "category": "Tea",
            "image_url": "https://images.unsplash.com/photo-1556679343-c7306c1976bc?auto=format&fit=crop&w=800&q=80",
            "is_popular": False
        },
        {
            "id": "dish_iced_tea",
            "name": "Iced Tea",
            "description": "Chilled tea perfect for hot days",
            "price": 20,
            "category": "Tea",
            "image_url": "https://images.unsplash.com/photo-1499638309848-e9968540da83?auto=format&fit=crop&w=800&q=80",
            "is_popular": False
        },
        
        # Sandwich
        {
            "id": "dish_club_sandwich",
            "name": "Club Sandwich",
            "description": "Triple layer sandwich with chicken and veggies",
            "price": 50,
            "category": "Sandwich",
            "image_url": "https://images.unsplash.com/photo-1528735602780-2552fd46c7af?auto=format&fit=crop&w=800&q=80",
            "is_popular": True
        },
        {
            "id": "dish_veg_sandwich",
            "name": "Veg Sandwich",
            "description": "Fresh vegetables with tangy chutney",
            "price": 50,
            "category": "Sandwich",
            "image_url": "https://images.unsplash.com/photo-1509722747041-616f39b57569?auto=format&fit=crop&w=800&q=80",
            "is_popular": False
        },
        {
            "id": "dish_grilled_sandwich",
            "name": "Grilled Sandwich",
            "description": "Crispy grilled sandwich with cheese",
            "price": 50,
            "category": "Sandwich",
            "image_url": "https://images.unsplash.com/photo-1621852004146-75d47c57e990?auto=format&fit=crop&w=800&q=80",
            "is_popular": False
        },
        {
            "id": "dish_paneer_sandwich",
            "name": "Paneer Sandwich",
            "description": "Grilled sandwich with spiced paneer",
            "price": 50,
            "category": "Sandwich",
            "image_url": "https://images.unsplash.com/photo-1553909489-cd47e0907980?auto=format&fit=crop&w=800&q=80",
            "is_popular": False
        },
        
        # Cookies
        {
            "id": "dish_choco_chip",
            "name": "Chocolate Chip Cookies",
            "description": "Classic cookies with chocolate chips",
            "price": 30,
            "category": "Cookies",
            "image_url": "https://images.unsplash.com/photo-1499636136210-6f4ee915583e?auto=format&fit=crop&w=800&q=80",
            "is_popular": False
        },
        {
            "id": "dish_oatmeal_cookies",
            "name": "Oatmeal Cookies",
            "description": "Healthy oatmeal cookies with raisins",
            "price": 30,
            "category": "Cookies",
            "image_url": "https://images.unsplash.com/photo-1590841609987-4ac211afdde1?auto=format&fit=crop&w=800&q=80",
            "is_popular": False
        },
        {
            "id": "dish_butter_cookies",
            "name": "Butter Cookies",
            "description": "Melt-in-mouth butter cookies",
            "price": 30,
            "category": "Cookies",
            "image_url": "https://images.unsplash.com/photo-1558961363-fa8fdf82db35?auto=format&fit=crop&w=800&q=80",
            "is_popular": False
        },
        {
            "id": "dish_double_chocolate",
            "name": "Double Chocolate Cookies",
            "description": "Rich chocolate cookies for chocolate lovers",
            "price": 30,
            "category": "Cookies",
            "image_url": "https://images.unsplash.com/photo-1606890737304-57a1ca8a5b62?auto=format&fit=crop&w=800&q=80",
            "is_popular": False
        },
        
        # Pizza
        {
            "id": "dish_margherita",
            "name": "Margherita Pizza",
            "description": "Classic pizza with cheese and tomato sauce",
            "price": 100,
            "category": "Pizza",
            "image_url": "https://images.unsplash.com/photo-1574071318508-1cdbab80d002?auto=format&fit=crop&w=800&q=80",
            "is_popular": True
        },
        {
            "id": "dish_pepperoni",
            "name": "Pepperoni Pizza",
            "description": "Loaded with pepperoni and cheese",
            "price": 100,
            "category": "Pizza",
            "image_url": "https://images.unsplash.com/photo-1628840042765-356cda07504e?auto=format&fit=crop&w=800&q=80",
            "is_popular": False
        },
        {
            "id": "dish_veg_pizza",
            "name": "Veggie Pizza",
            "description": "Fresh vegetables on cheese base",
            "price": 100,
            "category": "Pizza",
            "image_url": "https://images.unsplash.com/photo-1511689660979-10d2b1aada49?auto=format&fit=crop&w=800&q=80",
            "is_popular": False
        },
        {
            "id": "dish_farmhouse",
            "name": "Farmhouse Pizza",
            "description": "Garden fresh vegetables with cheese",
            "price": 100,
            "category": "Pizza",
            "image_url": "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?auto=format&fit=crop&w=800&q=80",
            "is_popular": False
        },
        
        # Burger
        {
            "id": "dish_classic_burger",
            "name": "Classic Burger",
            "description": "Juicy beef patty with lettuce and tomato",
            "price": 70,
            "category": "Burger",
            "image_url": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=800&q=80",
            "is_popular": True
        },
        {
            "id": "dish_cheese_burger",
            "name": "Cheese Burger",
            "description": "Classic burger with extra cheese",
            "price": 70,
            "category": "Burger",
            "image_url": "https://images.unsplash.com/photo-1550547660-d9450f859349?auto=format&fit=crop&w=800&q=80",
            "is_popular": False
        },
        {
            "id": "dish_veg_burger",
            "name": "Veg Burger",
            "description": "Crispy vegetable patty burger",
            "price": 70,
            "category": "Burger",
            "image_url": "https://images.unsplash.com/photo-1520072959219-c595dc870360?auto=format&fit=crop&w=800&q=80",
            "is_popular": False
        },
        {
            "id": "dish_chicken_burger",
            "name": "Chicken Burger",
            "description": "Grilled chicken patty with special sauce",
            "price": 70,
            "category": "Burger",
            "image_url": "https://images.unsplash.com/photo-1606755962773-d324e0a13086?auto=format&fit=crop&w=800&q=80",
            "is_popular": False
        }
    ]
    
    for dish in dishes:
        supabase.table("dishes").insert(dish).execute()
    print("Dishes seeded")
    
    print("\nDatabase seeded successfully!")

if __name__ == "__main__":
    seed_database()
