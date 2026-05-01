# cafeteria
Cafetaria – Smart Cafeteria Ordering Web App

Cafetaria is a full-stack cafeteria ordering web application designed to simplify food ordering in cafeterias and college canteens.
Customers can browse the menu, add items to a cart, enter their table number, and place orders seamlessly — without any login or authentication.

The project focuses on a clean UI, smooth user experience, and real-world usability.

* Features

Animated splash screen using Lottie

Warm coffee-brown themed UI (light mode)

Category-based menu browsing

Popular dishes auto-scroll carousel

Cart with quantity control and auto total calculation

Mandatory table number before order placement

Internal dashboard notifications for new orders

Order history and feedback sections

Fully responsive web application

* Menu Categories & Prices
Category	Price (₹)
Pizza	100
Burger	70
Sandwich	50
Coffee	50
Cookies	30
Tea	20

Prices are category-based and can be updated later from the backend.

* Tech Stack

Frontend: FlutterFlow (Flutter Web)

Backend: FlutterFlow Backend / Firebase

Database: Firestore

State Management: FlutterFlow App State

Animations: Lottie (.json)

* Application Flow

App opens with a splash screen (2 seconds)

User lands on Home Page

Browse menu by category or popular dishes

Add items to cart and select quantities

Enter table number

Place order

Order saved to backend and shown in dashboard notifications

* Internal Order Notification

After an order is placed, an internal dashboard alert is generated:

“Order placed from table ___.”

Alerts appear in:

Dashboard

Order history

No SMS, email, or third-party messaging services are used.

* Backend Collections

Dishes

name, category, price, image, description, isPopular

Orders

tableNumber, totalAmount, timestamp

OrderItems

orderId, dishName, price, quantity

Notifications

message, timestamp, isRead

* Future Enhancements

Admin control panel

Online payment gateway

Kitchen order display screen

Live order tracking

Multi-branch cafeteria support

preview link
https://cafeshop-ordering.preview.emergentagent.com/

Author
Rithesh 
B.Tech Student | Full-Stack & Flutter Enthusiast
