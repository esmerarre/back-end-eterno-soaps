# seed.py
from app.db import SessionLocal
from app.models.category import Category
from app.models.product import Product
from app.models.product_variant import ProductVariant

def seed_database():
    db = SessionLocal()

    try:
        # ---------- CATEGORY ----------
        category_data = [
            {"name": "Body", "description": "Body soaps"},
            {"name": "Face", "description": "Facial soaps"},
            {"name": "None", "description": "No specific category"}
        ]

        categories = []
        for data in category_data:
            cat = Category(**data)
            db.add(cat)
            categories.append(cat)

        db.commit()
        category_map = {c.name: c.id for c in categories}

        # ---------- PRODUCTS ----------
        products_data = [
            {
                "name": "Cottonwood",
                "description": "A soothing blend of natural herbs for gentle cleansing.",
                "category_id": category_map["Body"],
                "ingredients": ["Cottonwood Leaves", "Clove", "Cinnamon", "Bay Leaves", "Rosemary"]
            },
            {
                "name": "Cactus",
                "description": "Hydrating cactus soap infused with honey and Vitamin E.",
                "category_id": category_map["Body"],
                "ingredients": ["Cactus", "Honey", "Vitamin E", "Essential oils"]
            },
            {
                "name": "Saffron",
                "description": "Luxurious saffron and oats soap for radiant skin.",
                "category_id": category_map["Face"],
                "ingredients": ["Saffron", "Oats", "Tapioca", "Vitamin E", "Essential oils"]
            },
            {
                "name": "Aloe Vera",
                "description": "Relaxing lavender and aloe blend for sensitive skin.",
                "category_id": category_map["Face"],
                "ingredients": ["Lavender", "Turmeric", "Aloe Vera", "Calendula"]
            },
            {
                "name": "Spirulina, Aloe and Chamomile",
                "description": "Nourishing spirulina soap for soft, balanced skin.",
                "category_id": category_map["Face"],
                "ingredients": ["Spirulina", "Aloe Vera", "Chamomile", "Essential oils"]
            },
            {
                "name": "Kojic Acid",
                "description": "Brightening, fragrance-free soap with natural exfoliants.",
                "category_id": category_map["Face"],
                "ingredients": ["Kojic Acid", "Turmeric", "Rice Powder"]
            },
            {
                "name": "Activated Charcoal and Turmeric",
                "description": "Charcoal and turmeric soap for a gentle detox.",
                "category_id": category_map["Body"],
                "ingredients": ["Activated Charcoal", "Turmeric", "Essential Oils"]
            },
            {
                "name": "Oats, Honey, and Turmeric",
                "description": "Moisturizing honey and oats soap for soft skin.",
                "category_id": category_map["Body"],
                "ingredients": ["Oats", "Honey", "Turmeric"]
            },
            {
                "name": "Rose and Aloe",
                "description": "Romantic rose-infused soap for daily pampering.",
                "category_id": category_map["Face"],
                "ingredients": ["Rose petals", "Aloe Vera", "Essential Oils", "Vitamin E"]
            },
            {
                "name": "Turmeric",
                "description": "Brightening soap that helps even skin tone and glow.",
                "category_id": category_map["Face"],
                "ingredients": ["Turmeric"]
            },
            {
                "name": "Cucumber",
                "description": "Cool, refreshing cleanse for calm, hydrated skin.",
                "category_id": category_map["Face"],
                "ingredients": ["Cucumber"]
            },
            {
                "name": "Coffee and Oats",
                "description": "Gently exfoliates while energizing tired skin.",
                "category_id": category_map["Body"],
                "ingredients": ["Coffee", "Oats"]
            },
            {
                "name": "Quinoa",
                "description": "Nutrient-rich soap that supports soft, healthy skin.",
                "category_id": category_map["Body"],
                "ingredients": ["Quinoa"]
            },
            {
                "name": "Green Tea",
                "description": "Antioxidant-packed cleanse that refreshes and protects.",
                "category_id": category_map["Face"],
                "ingredients": ["Aloe Vera", "Green Tea"]
            },
            {
                "name": "Rice and Oats",
                "description": "Mild exfoliation for smooth, balanced skin.",
                "category_id": category_map["Body"],
                "ingredients": ["Rice", "Oats"]
            },
            {
                "name": "French Green Clay",
                "description": "Deep-cleansing soap that detoxifies and purifies pores.",
                "category_id": category_map["Face"],
                "ingredients": ["French Green Clay"]
            },
            {
                "name": "Oats and Sweet Almond Oil",
                "description": "Moisturizing for dry skin.",
                "category_id": category_map["Body"],
                "ingredients": ["Oats", "Almond Oil"]
            },
        ]

        products = []
        for data in products_data:
            product = Product(**data)
            db.add(product)
            products.append(product)

        db.commit()
        product_map = {p.name: p.id for p in products}

        # ---------- VARIANTS ----------
        variants_data = [
            ("Cottonwood", "Medium", "Flower", 8.00, 10),
            ("Cottonwood", "Large", "Massage Bar", 12.00, 10),
            ("Cactus", "Small", None, 5.00, 15),
            ("Saffron", "Small", None, 5.00, 4),
            ("Saffron", "Medium", "Square", 10.00, 10),
            ("Aloe Vera", "Medium", "Flower", 8.00, 7),
            ("Aloe Vera", "Large", "Rectangle", 10.00, 14),
            ("Spirulina, Aloe and Chamomile", "Small", None, 5.00, 3),
            ("Spirulina, Aloe and Chamomile", "Medium", "Flower", 8.00, 7),
            ("Kojic Acid", "Large", "Rectangle", 15.00, 12),
            ("Kojic Acid", "Medium", "Oval", 6.00, 6),
            ("Activated Charcoal and Turmeric", "Large", "Massage Bar", 12.00, 7),
            ("Activated Charcoal and Turmeric", "Small", "Round", 5.00, 3),
            ("Oats, Honey, and Turmeric", "Large", "Rectangle", 10.00, 3),
            ("Oats, Honey, and Turmeric", "Medium", "Bee Honeycomb", 8.00, 2),
            ("Rose and Aloe", "Medium", "Flower", 8.00, 7),
            ("Rose and Aloe", "Medium", "Square", 10.00, 8),
            ("Turmeric", "Large", "Rectangle", 10.00, 8),
            ("Turmeric", "Small", None, 5.00, 7),
            ("Cucumber", "Small", None, 5.00, 6),
            ("Coffee and Oats", "Small", None, 5.00, 4),
            ("Coffee and Oats", "Large", "Massage Bar", 12.00, 3),
            ("Quinoa", "Medium", "Square", 8.00, 2),
            ("Quinoa", "Medium", "Oval", 6.00, 2),
            ("Green Tea", "Medium", "Square", 8.00, 8),
            ("Green Tea", "Small", "Round", 5.00, 7),
            ("Rice and Oats", "Small", "Round", 5.00, 8),
            ("Rice and Oats", "Medium", "Square", 10.00, 8),
            ("French Green Clay", "Medium", "Square", 8.00, 8),
            ("French Green Clay", "Big", "Round", 10.00, 8),
            ("French Green Clay", "Small", "Round", 5.00, 8),
            ("Oats and Sweet Almond Oil", "Medium", "Oval", 6.00, 8),
            ("Oats and Sweet Almond Oil", "Small", "Round", 5.00, 8),
        ]

        for name, size, shape, price, stock in variants_data:
            variant = ProductVariant(
                product_id=product_map[name],
                size=size,
                shape=shape,  # shape can be None
                price=price,
                stock_quantity=stock
            )
            db.add(variant)

        db.commit()
        print("✅ Database seeded successfully!")

    except Exception as e:
        db.rollback()
        print("❌ Seeding failed:", e)
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
