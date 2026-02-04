# seed.py
from app.db import SessionLocal
from app.models.category import Category
from app.models.product import Product
from app.models.product_variant import ProductVariant
from app.models.product_categories import association_table


def seed_database():
    db = SessionLocal()

    try:
        # ---------- CATEGORIES ----------
        category_data = [
            {"name": "Cleansing", "description": "Effectively removes impurities while refreshing the skin."},
            {"name": "Calming", "description": "Soothes skin and helps reduce irritation or redness."},
            {"name": "Moisturizing", "description": "Provides lasting hydration to keep skin soft and smooth."},
            {"name": "Brightening", "description": "Helps improve dull skin for a radiant look."},
            {"name": "Exfoliating", "description": "Gently removes dead skin cells."},
            {"name": "Unscented", "description": "Free from added fragrance."},
            {"name": "Sensitive skin", "description": "Gentle and suitable for sensitive skin."},
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
                "ingredients": ["Cottonwood Leaves", "Clove", "Cinnamon", "Bay Leaves", "Rosemary"],
            },
            {
                "name": "Cactus",
                "description": "Hydrating cactus soap infused with honey and Vitamin E.",
                "ingredients": ["Cactus", "Honey", "Vitamin E", "Essential oils"],
            },
            {
                "name": "Saffron",
                "description": "Luxurious saffron and oats soap for radiant skin.",
                "ingredients": ["Saffron", "Oats", "Tapioca", "Vitamin E", "Essential oils"],
            },
            {
                "name": "Aloe Vera",
                "description": "Relaxing lavender and aloe blend for sensitive skin.",
                "ingredients": ["Lavender", "Turmeric", "Aloe Vera", "Calendula"],
            },
            {
                "name": "Spirulina, Aloe and Chamomile",
                "description": "Nourishing spirulina soap for soft, balanced skin.",
                "ingredients": ["Spirulina", "Aloe Vera", "Chamomile", "Essential oils"],
            },
            {
                "name": "Kojic Acid",
                "description": "Brightening, fragrance-free soap with natural exfoliants.",
                "ingredients": ["Kojic Acid", "Turmeric", "Rice Powder"],
            },
            {
                "name": "Activated Charcoal",
                "description": "Charcoal soap for a gentle detox.",
                "ingredients": ["Activated Charcoal", "Turmeric", "Essential Oils"],
            },
            {
                "name": "Oats, Honey, and Turmeric",
                "description": "Moisturizing honey and oats soap for soft skin.",
                "ingredients": ["Oats", "Honey", "Turmeric"],
            },
            {
                "name": "Rose and Aloe",
                "description": "Romantic rose-infused soap for daily pampering.",
                "ingredients": ["Rose petals", "Aloe Vera", "Essential Oils", "Vitamin E"],
            },
            {
                "name": "Turmeric",
                "description": "Brightening soap that helps even skin tone and glow.",
                "ingredients": ["Turmeric"],
            },
            {
                "name": "Cucumber",
                "description": "Cool, refreshing cleanse for calm, hydrated skin.",
                "ingredients": ["Cucumber"],
            },
            {
                "name": "Coffee and Oats",
                "description": "Gently exfoliates while energizing tired skin.",
                "ingredients": ["Coffee", "Oats"],
            },
            {
                "name": "Quinoa",
                "description": "Nutrient-rich soap that supports soft, healthy skin.",
                "ingredients": ["Quinoa"],
            },
            {
                "name": "Green Tea",
                "description": "Antioxidant-packed cleanse that refreshes and protects.",
                "ingredients": ["Aloe Vera", "Green Tea"],
            },
            {
                "name": "Rice and Oats",
                "description": "Mild exfoliation for smooth, balanced skin.",
                "ingredients": ["Rice", "Oats"],
            },
            {
                "name": "French Green Clay",
                "description": "Deep-cleansing soap that detoxifies and purifies pores.",
                "ingredients": ["French Green Clay"],
            },
            {
                "name": "Oats and Sweet Almond Oil",
                "description": "Moisturizing for dry skin.",
                "ingredients": ["Oats", "Almond Oil"],
            },
        ]

        products = []
        for data in products_data:
            product = Product(**data)
            db.add(product)
            products.append(product)

        db.commit()
        product_map = {p.name: p.id for p in products}

        # ---------- PRODUCT ↔ CATEGORY ----------
        # Map product IDs to lists of category names
        product_category_map = {
            1: ["Cleansing", "Calming", "Sensitive skin"],   # Cottonwood
            2: ["Moisturizing", "Cleansing"],                # Cactus
            3: ["Moisturizing", "Brightening"],              # Saffron
            4: ["Moisturizing", "Calming", "Sensitive skin"], # Aloe Vera
            5: ["Moisturizing", "Sensitive skin", "Calming"], # Spirulina, Aloe and Chamomile
            6: ["Cleansing", "Brightening", "Unscented"],    # Kojic Acid
            7: ["Brightening", "Cleansing", "Exfoliating"],  # Activated Charcoal and Turmeric
            8: ["Calming", "Brightening", "Moisturizing"],   # Oats, Honey, and Turmeric
            9: ["Calming", "Moisturizing"],                  # Rose and Aloe
            10: ["Cleansing", "Brightening"],                # Turmeric
            11: ["Moisturizing", "Sensitive skin", "Calming"], # Cucumber
            12: ["Cleansing", "Exfoliating"],                # Coffee and Oats
            13: ["Cleansing", "Moisturizing"],               # Quinoa
            14: ["Calming", "Cleansing"],                    # Green Tea
            15: ["Calming", "Exfoliating", "Sensitive skin"], # Rice and Oats
            16: ["Cleansing", "Exfoliating"],                # French Green Clay
            17: ["Calming", "Moisturizing", "Sensitive skin"], # Oats and Sweet Almond Oil
        }

        # Ensure every product is in at least one category
        all_product_ids = set(product_map.values())
        mapped_product_ids = set(product_category_map.keys())
        unmapped_product_ids = all_product_ids - mapped_product_ids

        # Assign a default category (e.g., 'Cleansing') if a product has no categories
        default_category_name = "Cleansing"
        default_category_id = category_map.get(default_category_name)

        for product_id, category_names in product_category_map.items():
            if not category_names:
                # If no categories, assign default
                if default_category_id:
                    db.execute(
                        association_table.insert().values(
                            product_id=product_id,
                            category_id=default_category_id,
                        )
                    )
            else:
                for category_name in category_names:
                    category_id = category_map.get(category_name)
                    if category_id:
                        db.execute(
                            association_table.insert().values(
                                product_id=product_id,
                                category_id=category_id,
                            )
                        )

        # For any product not in the map, assign default category
        for product_id in unmapped_product_ids:
            if default_category_id:
                db.execute(
                    association_table.insert().values(
                        product_id=product_id,
                        category_id=default_category_id,
                    )
                )

        db.commit()

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
            ("Activated Charcoal", "Large", "Massage Bar", 12.00, 7),
            ("Activated Charcoal", "Small", "Round", 5.00, 3),
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
            ("French Green Clay", "Large", "Round", 10.00, 8),
            ("French Green Clay", "Small", "Round", 5.00, 8),
            ("Oats and Sweet Almond Oil", "Medium", "Oval", 6.00, 8),
            ("Oats and Sweet Almond Oil", "Small", "Round", 5.00, 8),
        ]

        for name, size, shape, price, stock in variants_data:
            db.add(
                ProductVariant(
                    product_id=product_map[name],
                    size=size,
                    shape=shape,
                    price=price,
                    stock_quantity=stock,
                )
            )

        db.commit()
        print("✅ Database seeded successfully!")

    except Exception as e:
        db.rollback()
        print("❌ Seeding failed:", e)
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
