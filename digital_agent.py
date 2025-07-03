# Quick Start Digital Product Agent
# Save as: digital_agent.py

import anthropic
import json
import time
from datetime import datetime


class SimpleProductAgent:
    def __init__(self, api_key):
        self.client = anthropic.Anthropic(api_key=api_key)
        print("🤖 Agent initialized successfully!")

    def find_trending_opportunities(self):
        """Find profitable digital product opportunities"""
        print("🔍 Scanning for trending opportunities...")

        prompt = """
        You are a digital product opportunity scanner. Find 3 HIGH-PROFIT digital product ideas for January 2025.

        Consider:
        - New Year productivity trends
        - Business planning season
        - AI/automation interest
        - Side hustle demand

        Return ONLY valid JSON (no other text):
        [
            {
                "keyword": "specific trend",
                "score": 85,
                "opportunity": "high", 
                "price": 29.99,
                "audience": "target buyer",
                "reasoning": "why profitable"
            }
        ]
        """

        try:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1500,
                messages=[{"role": "user", "content": prompt}]
            )

            content = response.content[0].text
            # Extract JSON
            start = content.find('[')
            end = content.rfind(']') + 1

            if start >= 0 and end > start:
                json_str = content[start:end]
                opportunities = json.loads(json_str)
                print(f"✅ Found {len(opportunities)} opportunities!")
                return opportunities
            else:
                print("❌ Could not parse opportunities")
                return []

        except Exception as e:
            print(f"❌ Error finding opportunities: {e}")
            return []

    def create_product(self, opportunity):
        """Create a complete digital product"""
        print(f"🏭 Creating product for: {opportunity['keyword']}")

        prompt = f"""
        Create a complete digital product for: {opportunity['keyword']}
        Target: {opportunity['audience']}
        Price: ${opportunity['price']}

        Create a valuable digital guide/ebook with:
        1. Catchy title
        2. Sales description 
        3. Detailed outline (10+ sections)
        4. First chapter content (500+ words)
        5. Marketing keywords

        Return ONLY valid JSON:
        {{
            "title": "Product Title",
            "description": "Sales copy description",
            "outline": ["Section 1", "Section 2", "..."],
            "sample_content": "First chapter content...",
            "keywords": ["keyword1", "keyword2"],
            "platforms": ["Etsy", "Gumroad"]
        }}

        Make it genuinely valuable and worth ${opportunity['price']}.
        """

        try:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=3000,
                messages=[{"role": "user", "content": prompt}]
            )

            content = response.content[0].text
            start = content.find('{')
            end = content.rfind('}') + 1

            if start >= 0 and end > start:
                json_str = content[start:end]
                product = json.loads(json_str)
                print(f"✅ Product created: {product['title']}")
                return product
            else:
                print("❌ Could not parse product")
                return None

        except Exception as e:
            print(f"❌ Error creating product: {e}")
            return None

    def create_listings(self, product, price):
        """Create marketplace listings"""
        print("🛍️ Creating marketplace listings...")

        prompt = f"""
        Create optimized marketplace listings for:
        Title: {product['title']}
        Description: {product['description']}
        Price: ${price}

        Create listings for:
        1. Etsy (title + tags + description)
        2. Gumroad (title + description)

        Return ONLY valid JSON:
        {{
            "etsy": {{
                "title": "SEO optimized title (under 140 chars)",
                "tags": ["tag1", "tag2", "tag3"],
                "description": "Compelling Etsy description"
            }},
            "gumroad": {{
                "title": "Gumroad title",
                "description": "Gumroad sales description"
            }}
        }}

        Optimize for sales conversion and platform algorithms.
        """

        try:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )

            content = response.content[0].text
            start = content.find('{')
            end = content.rfind('}') + 1

            if start >= 0 and end > start:
                json_str = content[start:end]
                listings = json.loads(json_str)
                print("✅ Listings created!")
                return listings
            else:
                print("❌ Could not parse listings")
                return None

        except Exception as e:
            print(f"❌ Error creating listings: {e}")
            return None

    def save_results(self, opportunities, products):
        """Save results to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"digital_products_{timestamp}.json"

        results = {
            "timestamp": timestamp,
            "opportunities": opportunities,
            "products": products
        }

        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)

        print(f"💾 Results saved to: {filename}")
        return filename

    def run_full_cycle(self):
        """Run complete product creation cycle"""
        print("🚀 Starting Digital Product Creation Cycle...")
        print("=" * 50)

        # Step 1: Find opportunities
        opportunities = self.find_trending_opportunities()
        if not opportunities:
            print("❌ No opportunities found. Exiting.")
            return

        products = []

        # Step 2: Create products for top opportunities
        for i, opp in enumerate(opportunities[:2]):  # Process top 2
            print(f"\n📦 Processing opportunity {i + 1}/{len(opportunities[:2])}")
            print(f"Topic: {opp['keyword']}")
            print(f"Score: {opp['score']}")
            print(f"Price: ${opp['price']}")

            # Create product
            product = self.create_product(opp)
            if product:
                # Create listings
                listings = self.create_listings(product, opp['price'])

                # Combine all data
                complete_product = {
                    "opportunity": opp,
                    "product": product,
                    "listings": listings,
                    "created_at": datetime.now().isoformat()
                }

                products.append(complete_product)

                print(f"✅ Complete product package created!")
                print(f"📝 Title: {product['title']}")
                print(f"💰 Price: ${opp['price']}")
                print("-" * 30)

            # Rate limiting
            time.sleep(5)

        # Step 3: Save everything
        if products:
            filename = self.save_results(opportunities, products)

            print("\n🎉 CYCLE COMPLETE!")
            print(f"📊 Created {len(products)} complete products")
            print(f"💾 Saved to: {filename}")
            print("\n📋 Next steps:")
            print("1. Review the generated products")
            print("2. Create accounts on Etsy/Gumroad")
            print("3. List your first product")
            print("4. Monitor sales and optimize")
        else:
            print("❌ No products were created successfully")


# Main execution
def main():
    print("🚀 Digital Product Agent - Quick Start")
    print("=" * 40)

    # Get API key from user
    api_key = input("📝 Enter your Claude API key: ").strip()

    if not api_key:
        print("❌ API key is required!")
        return

    try:
        # Initialize agent
        agent = SimpleProductAgent(api_key)

        # Run the cycle
        agent.run_full_cycle()

    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Make sure your API key is correct and you have credits")


if __name__ == "__main__":
    main()