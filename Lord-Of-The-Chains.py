import time
import random

class Customer:
    def __init__(self, name, x, y):
        self.name = name
        self.location = (x, y)
        self.order_history = []

    def place_order(self, restaurant, items, priority=False):
        order = Order(self, restaurant, items, priority)
        self.order_history.append(order)
        restaurant.receive_order(order)
        print(f"\n✅ {self.name} placed an order at {restaurant.name}. Priority Order: {priority}\n")

    def check_order_status(self, order):
        print(f"📌 Current status of your order: {order.status}")

class Restaurant:
    def __init__(self, name, x, y, menu):
        self.name = name
        self.location = (x, y)
        self.menu = menu
        self.orders = []

    def receive_order(self, order):
        self.orders.append(order)
        print(f"\n📩 Order received at {self.name}. Please wait while we process it...\n")

    def accept_order(self, order):
        order.status = "Accepted"
        time.sleep(2)
        print(f"\n🍽️ {self.name} has accepted the order! Preparing your food now...\n")
        return True

    def reject_order(self, order):
        order.status = "Rejected"
        print(f"\n⚠️ Sorry! {self.name} couldn't accept this order at the moment.\n")
        return False

class Order:
    def __init__(self, customer, restaurant, items, priority):
        self.customer = customer
        self.restaurant = restaurant
        self.items = items
        self.priority = priority
        self.status = "Initiated"
        self.assigned_driver = None
        self.fee = self.calculate_fee()

    def update_status(self, new_status):
        self.status = new_status
        print(f"🆕 Order Status Updated: {self.status}\n")

    def calculate_fee(self):
        x1, y1 = self.customer.location
        x2, y2 = self.restaurant.location
        return round(((x1 - x2)**2 + (y1 - y2)**2) ** 0.5 * 10, 2)

class DeliveryAgent:
    def __init__(self, name, x, y):
        self.name = name
        self.location = (x, y)
        self.status = "Available"
        self.current_order = None

    def assign_order(self, order):
        if self.status == "Available":
            self.current_order = order
            self.status = "BUSY"
            order.assigned_driver = self
            order.update_status("Deployed")
            print(f"\n🚴 {self.name} is on the way to pick up your order from {order.restaurant.name}!\n")

    def deliver_order(self):
        if self.current_order:
            time.sleep(3)  # Simulating travel time
            self.current_order.update_status("Delivered")
            print(f"\n✅ Order successfully delivered by {self.name}!\n")
            self.status = "Available"
            self.current_order = None

class DeliverySystem:
    def __init__(self):
        self.customers = []
        self.restaurants = []
        self.delivery_agents = []
        self.orders = []

    def add_customer(self, customer):
        self.customers.append(customer)

    def add_restaurant(self, restaurant):
        self.restaurants.append(restaurant)

    def add_delivery_agent(self, agent):
        self.delivery_agents.append(agent)

    def process_order(self, order):
        if order.restaurant.accept_order(order):
            self.orders.append(order)
            self.assign_driver(order)

    def assign_driver(self, order):
        available_drivers = [d for d in self.delivery_agents if d.status == "Available"]
        if not available_drivers:
            print("🚫 No drivers available at the moment.\n")
            return

        # Assign priority orders first, then normal ones
        priority_orders = [o for o in self.orders if o.priority and not o.assigned_driver]
        non_priority_orders = [o for o in self.orders if not o.priority and not o.assigned_driver]
        sorted_orders = priority_orders + non_priority_orders

        for order in sorted_orders:
            nearest_driver = min(available_drivers, key=lambda d: ((d.location[0] - order.restaurant.location[0])**2 + (d.location[1] - order.restaurant.location[1])**2) ** 0.5)
            nearest_driver.assign_order(order)

    def simulate_delivery(self):
        busy_drivers = [d for d in self.delivery_agents if d.status == "BUSY"]
        for driver in busy_drivers:
            driver.deliver_order()

class CustomerCare:
    def __init__(self):
        self.active_tickets = {}  
        self.resolved_tickets = []  

    def submit_ticket(self, customer, issue):
        ticket_id = f"CC-{len(self.active_tickets) + 1}"
        self.active_tickets[ticket_id] = {"customer": customer.name, "issue": issue}
        print(f"\n💬 Ticket {ticket_id} submitted by {customer.name}: {issue}\n")

    def respond_ticket(self, ticket_id, response):
        if ticket_id in self.active_tickets:
            print(f"\n🛠️ Support Response to {ticket_id}: {response}\n")
            time.sleep(3)
        else:
            print(f"\n⚠️ Ticket {ticket_id} not found.\n")

    def resolve_ticket(self, ticket_id):
        if ticket_id in self.active_tickets:
            self.resolved_tickets.append(self.active_tickets.pop(ticket_id))
            print(f"\n✅ Ticket {ticket_id} has been successfully resolved!\n")

    def view_active_tickets(self):
        if self.active_tickets:
            print("\n📢 Active Customer Complaints:")
            for ticket_id, details in self.active_tickets.items():
                print(f"🔹 {ticket_id}: {details['customer']} - {details['issue']}")
        else:
            print("\n🚀 No unresolved issues at the moment!")

# Initialize the system
delivery_system = DeliverySystem()

print("Welcome to the Food Delivery Simulation 🍽️🚀")

name = input("Enter your name: ")
customer = Customer(name, 10, 5)
delivery_system.add_customer(customer)

print("\n📍 Available Restaurants:")
restaurants = {
    "Dominoes": Restaurant("Dominoes", 5, 5, {"Pizza": 100, "Pasta": 40}),
    "Burger Singh": Restaurant("Burger Singh", 2, 6, {"Burger": 60, "Fries": 35}),
}

for index, r in enumerate(restaurants.keys(), 1):
    print(f"{index}. {r}")

selected_restaurant = input("\nEnter restaurant name: ")
restaurant = restaurants.get(selected_restaurant)

if not restaurant:
    print("🚨 Invalid choice. Exiting...")
    exit()

prio = input("Is this a priority order? (yes/no): ").strip().lower() == "yes"

# Delivery boys
agent1 = DeliveryAgent("Rakesh", 5, 5)
agent2 = DeliveryAgent("Sonu", 2, 6)
delivery_system.add_delivery_agent(agent1)
delivery_system.add_delivery_agent(agent2)

# Place order
customer.place_order(restaurant, ["Pizza"], priority=prio)

# Process orders
for order in restaurant.orders:
    delivery_system.process_order(order)

# Simulate delivery
delivery_system.simulate_delivery()

# Customer Care Service
customer_care = CustomerCare()
satisfaction = input("\nWas your delivery satisfactory? (yes/no): ").strip().lower()
if satisfaction == "no":
    complaint = input("Describe your issue: ")
    customer_care.submit_ticket(customer, complaint)
    customer_care.respond_ticket("CC-1", "We're investigating your concern!")
    customer_care.resolve_ticket("CC-1")

customer_care.view_active_tickets()
