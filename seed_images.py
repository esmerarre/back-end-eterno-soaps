# seed_images.py
from app.db import SessionLocal
from app.models.product import Product
from app.models.product_variant import ProductVariant
from sqlalchemy import select

def seed_image_keys():
    """
    Populate img_key columns for products and product variants.
    Priority for product default image: small > medium > large
    """
    db = SessionLocal()

    try:
        # Image mapping: product_name -> { size-shape: key }
        # Note: Keys are relative paths without bucket prefix
        image_map = {
            "Spirulina, Aloe and Chamomile": {
                "product": "products/algae-spirulina-small.jpeg",  # small exists
                "small": "products/algae-spirulina-small.jpeg",
                "medium-flower": "products/algae-spirulina-medium-fl.jpeg",
            },
            "Aloe Vera": {
                "product": "products/aloe-vera-medium-fl.jpeg",  # no small, use medium
                "medium-flower": "products/aloe-vera-medium-fl.jpeg",
                "large-rectangle": "products/aloe-vera-large-block.jpeg",
            },
            "Cactus": {
                "product": "products/cactus-small.jpeg",  # small exists
                "small": "products/cactus-small.jpeg",
            },
            "Activated Charcoal and Turmeric": {
                "product": "products/charcoal-small.jpeg",  # small exists
                "small-round": "products/charcoal-small.jpeg",
                "large-massage bar": "products/charcoal-large-mb.jpeg",
            },
            "Coffee and Oats": {
                "product": "products/coffee-oats-small.jpeg",  # small exists
                "small": "products/coffee-oats-small.jpeg",
                "large-massage bar": "products/coffee-oats-large-mb.jpeg",
            },
            "Cottonwood": {
                "product": "products/cottonwood-medium-fl.jpeg",  # no small, use medium
                "medium-flower": "products/cottonwood-medium-fl.jpeg",
                "large-massage bar": "products/cottonwood-large-mb.jpeg",
            },
            "Cucumber": {
                "product": "products/cucumber-small.jpeg",  # small exists
                "small": "products/cucumber-small.jpeg",
            },
            "French Green Clay": {
                "product": "products/french-green-clay-medium-sq.jpeg",  # no small for this exact product
                "small-round": "products/french-green-clay-medium-sq.jpeg",  # Use medium as fallback
                "medium-square": "products/french-green-clay-medium-sq.jpeg",
                "big-round": "products/french-green-clay-medium-sq.jpeg",  # Use medium as fallback
            },
            "Green Tea": {
                "product": "products/green-tea-small.jpeg",  # small exists
                "small-round": "products/green-tea-small.jpeg",
                "medium-square": "products/green-tea-small.jpeg",  # Use small as fallback
            },
            "Kojic Acid": {
                "product": "products/kojic-medium-oval.jpeg",  # no small, use medium
                "medium-oval": "products/kojic-medium-oval.jpeg",
                "large-rectangle": "products/kojic-large-block.jpeg",
            },
            "Oats, Honey, and Turmeric": {
                "product": "products/oats-honey-tumeric-large-block.jpeg",  # no small/medium bee, use large
                "large-rectangle": "products/oats-honey-tumeric-large-block.jpeg",
                "medium-bee honeycomb": "products/oats-honey-tumeric-medium-bee.jpeg",
            },
            "Oats and Sweet Almond Oil": {
                "product": "products/oats-sweet-almond-small.jpeg",  # small exists
                "small-round": "products/oats-sweet-almond-small.jpeg",
                "medium-oval": "products/oats-sweet-almond-small.jpeg",  # Use small as fallback
            },
            "Rice and Oats": {
                "product": "products/rice-oats-small.jpeg",  # small exists
                "small-round": "products/rice-oats-small.jpeg",
                "medium-square": "products/rice-oats-medium-sq.jpeg",
            },
            "Rose and Aloe": {
                "product": "products/roses-aloe-medium-fl.jpeg",  # no small, use medium
                "medium-flower": "products/roses-aloe-medium-fl.jpeg",
                "medium-square": "products/roses-aloe-medium-fl.jpeg",  # Use flower for square variant
            },
            "Saffron": {
                "product": "products/saffron-medium-sq.jpeg",  # no small, use medium
                "small": "products/saffron-medium-sq.jpeg",  # Use medium as fallback
                "medium-square": "products/saffron-medium-sq.jpeg",
            },
            "Turmeric": {
                "product": "products/tumeric-small.jpeg",  # small exists
                "small": "products/tumeric-small.jpeg",
                "large-rectangle": "products/tumeric-large-block.jpeg",
            },
            "Quinoa": {
                "product": None,  # No corresponding images found
                "medium-square": None,
                "medium-oval": None,
            },
        }

        # Update products with default images
        products = db.execute(select(Product)).scalars().all()
        updated_products = 0
        
        for product in products:
            if product.name in image_map:
                product_img = image_map[product.name].get("product")
                if product_img:
                    product.img_key = product_img
                    updated_products += 1
                    print(f"✓ Product '{product.name}' -> {product_img}")
                else:
                    print(f"⚠ Product '{product.name}' has no matching image")
            else:
                print(f"⚠ Product '{product.name}' not in image mapping")

        db.commit()
        print(f"\n✅ Updated {updated_products} products with images")

        # Update product variants
        variants = db.execute(select(ProductVariant)).scalars().all()
        updated_variants = 0
        
        for variant in variants:
            product = db.get(Product, variant.product_id)
            if product and product.name in image_map:
                # Create variant key: "size-shape" or just "size"
                variant_key = variant.size.lower()
                if variant.shape:
                    variant_key = f"{variant.size.lower()}-{variant.shape.lower()}"
                
                variant_img = image_map[product.name].get(variant_key)
                if variant_img:
                    variant.img_key = variant_img
                    updated_variants += 1
                    print(f"✓ Variant '{product.name}' ({variant.size}, {variant.shape}) -> {variant_img}")
                else:
                    print(f"⚠ Variant '{product.name}' ({variant.size}, {variant.shape}) has no matching image")
        
        db.commit()
        print(f"\n✅ Updated {updated_variants} variants with images")
        print(f"\n🎉 Image seeding complete!")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Image seeding failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    seed_image_keys()
