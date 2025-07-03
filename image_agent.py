# Automated Etsy Image Creation Agent
# Save as: image_agent.py

import requests
import json
from PIL import Image, ImageDraw, ImageFont
import textwrap
import os


class EtsyImageAgent:
    def __init__(self):
        self.image_size = (1000, 1000)  # Square format for Etsy
        self.background_color = (255, 255, 255)  # White background
        self.primary_color = (30, 64, 175)  # Blue
        self.secondary_color = (107, 114, 128)  # Gray
        self.accent_color = (34, 197, 94)  # Green

    def create_main_image(self, product_data):
        """Create the main product image"""
        img = Image.new('RGB', self.image_size, self.background_color)
        draw = ImageDraw.Draw(img)

        # Load fonts (you may need to adjust font paths)
        try:
            title_font = ImageFont.truetype("arial.ttf", 80)
            subtitle_font = ImageFont.truetype("arial.ttf", 40)
            price_font = ImageFont.truetype("arial.ttf", 35)
        except:
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
            price_font = ImageFont.load_default()

        # Extract product info
        title = product_data['product']['title']
        price = product_data['opportunity']['price']

        # Main title (wrap text)
        main_title = "AI-POWERED\nPRODUCTIVITY\nMATRIX"

        # Calculate text positions
        y_pos = 150

        # Draw main title
        for line in main_title.split('\n'):
            bbox = draw.textbbox((0, 0), line, font=title_font)
            text_width = bbox[2] - bbox[0]
            x_pos = (self.image_size[0] - text_width) // 2
            draw.text((x_pos, y_pos), line, fill=self.primary_color, font=title_font)
            y_pos += 90

        # Subtitle
        subtitle = "For High-Performance Entrepreneurs"
        bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
        text_width = bbox[2] - bbox[0]
        x_pos = (self.image_size[0] - text_width) // 2
        draw.text((x_pos, y_pos + 50), subtitle, fill=self.secondary_color, font=subtitle_font)

        # Price
        price_text = f"${price} • Digital Download"
        bbox = draw.textbbox((0, 0), price_text, font=price_font)
        text_width = bbox[2] - bbox[0]
        x_pos = (self.image_size[0] - text_width) // 2
        draw.text((x_pos, y_pos + 150), price_text, fill=self.accent_color, font=price_font)

        # Add decorative elements
        self.add_decorative_elements(draw)

        return img

    def create_whats_included_image(self, product_data):
        """Create 'What's Included' image"""
        img = Image.new('RGB', self.image_size, self.background_color)
        draw = ImageDraw.Draw(img)

        try:
            title_font = ImageFont.truetype("arial.ttf", 60)
            text_font = ImageFont.truetype("arial.ttf", 35)
        except:
            title_font = ImageFont.load_default()
            text_font = ImageFont.load_default()

        # Title
        title = "WHAT'S INCLUDED"
        bbox = draw.textbbox((0, 0), title, font=title_font)
        text_width = bbox[2] - bbox[0]
        x_pos = (self.image_size[0] - text_width) // 2
        draw.text((x_pos, 80), title, fill=self.primary_color, font=title_font)

        # Checklist items
        items = [
            "✓ Complete AI Integration Guide",
            "✓ ChatGPT Workflow Templates",
            "✓ Task Automation Blueprints",
            "✓ Decision-Making Frameworks",
            "✓ 12 Comprehensive Chapters",
            "✓ Bonus Templates & Tools",
            "✓ Instant Digital Download"
        ]

        y_pos = 200
        for item in items:
            draw.text((100, y_pos), item, fill=self.secondary_color, font=text_font)
            y_pos += 60

        return img

    def create_benefits_image(self, product_data):
        """Create benefits/transformation image"""
        img = Image.new('RGB', self.image_size, self.background_color)
        draw = ImageDraw.Draw(img)

        try:
            title_font = ImageFont.truetype("arial.ttf", 50)
            text_font = ImageFont.truetype("arial.ttf", 35)
        except:
            title_font = ImageFont.load_default()
            text_font = ImageFont.load_default()

        # Title
        title = "TRANSFORM YOUR PRODUCTIVITY"
        bbox = draw.textbbox((0, 0), title, font=title_font)
        text_width = bbox[2] - bbox[0]
        x_pos = (self.image_size[0] - text_width) // 2
        draw.text((x_pos, 80), title, fill=self.primary_color, font=title_font)

        # Benefits
        benefits = [
            "🚀 10x Your Efficiency",
            "🤖 Master AI Tools",
            "⏰ Save 10+ Hours Weekly",
            "💰 Boost Revenue",
            "🎯 Stay Focused",
            "✨ Work Smarter Not Harder"
        ]

        y_pos = 200
        for benefit in benefits:
            draw.text((100, y_pos), benefit, fill=self.secondary_color, font=text_font)
            y_pos += 80

        return img

    def create_preview_image(self, product_data):
        """Create content preview image"""
        img = Image.new('RGB', self.image_size, self.background_color)
        draw = ImageDraw.Draw(img)

        try:
            title_font = ImageFont.truetype("arial.ttf", 60)
            text_font = ImageFont.truetype("arial.ttf", 30)
        except:
            title_font = ImageFont.load_default()
            text_font = ImageFont.load_default()

        # Title
        title = "INSIDE PREVIEW"
        bbox = draw.textbbox((0, 0), title, font=title_font)
        text_width = bbox[2] - bbox[0]
        x_pos = (self.image_size[0] - text_width) // 2
        draw.text((x_pos, 80), title, fill=self.primary_color, font=title_font)

        # Preview chapters
        chapters = [
            "Chapter 1: AI Productivity Fundamentals",
            "Chapter 5: Automation Workflows",
            "Chapter 8: Decision Making with AI",
            "Chapter 10: Data-Driven Analytics",
            "Chapter 12: Future-Proofing"
        ]

        y_pos = 200
        for chapter in chapters:
            # Wrap text if too long
            wrapped = textwrap.fill(chapter, width=35)
            for line in wrapped.split('\n'):
                draw.text((80, y_pos), line, fill=self.secondary_color, font=text_font)
                y_pos += 40
            y_pos += 20

        # Add page count
        page_text = "50+ Pages of Expert Content"
        bbox = draw.textbbox((0, 0), page_text, font=text_font)
        text_width = bbox[2] - bbox[0]
        x_pos = (self.image_size[0] - text_width) // 2
        draw.text((x_pos, 800), page_text, fill=self.accent_color, font=text_font)

        return img

    def create_instant_download_image(self, product_data):
        """Create instant download info image"""
        img = Image.new('RGB', self.image_size, self.background_color)
        draw = ImageDraw.Draw(img)

        try:
            title_font = ImageFont.truetype("arial.ttf", 60)
            text_font = ImageFont.truetype("arial.ttf", 35)
        except:
            title_font = ImageFont.load_default()
            text_font = ImageFont.load_default()

        # Title
        title = "INSTANT DOWNLOAD"
        bbox = draw.textbbox((0, 0), title, font=title_font)
        text_width = bbox[2] - bbox[0]
        x_pos = (self.image_size[0] - text_width) // 2
        draw.text((x_pos, 120), title, fill=self.primary_color, font=title_font)

        # Download details
        details = [
            "📱 Works on Any Device",
            "📄 PDF Format",
            "⚡ Immediate Access",
            "🔄 Lifetime Updates",
            "💾 Print Friendly"
        ]

        y_pos = 250
        for detail in details:
            draw.text((150, y_pos), detail, fill=self.secondary_color, font=text_font)
            y_pos += 80

        return img

    def add_decorative_elements(self, draw):
        """Add simple decorative elements"""
        # Add some simple shapes for visual appeal
        # Top corners
        draw.rectangle([20, 20, 120, 25], fill=self.accent_color)
        draw.rectangle([880, 20, 980, 25], fill=self.accent_color)

        # Bottom corners
        draw.rectangle([20, 975, 120, 980], fill=self.accent_color)
        draw.rectangle([880, 975, 980, 980], fill=self.accent_color)

    def generate_all_images(self, product_data, output_dir="etsy_images"):
        """Generate all Etsy images for a product"""

        # Create output directory
        os.makedirs(output_dir, exist_ok=True)

        print("🎨 Generating Etsy images...")

        # Generate all images
        images = {
            "main": self.create_main_image(product_data),
            "whats_included": self.create_whats_included_image(product_data),
            "benefits": self.create_benefits_image(product_data),
            "preview": self.create_preview_image(product_data),
            "instant_download": self.create_instant_download_image(product_data)
        }

        # Save all images
        for name, img in images.items():
            filename = f"{output_dir}/{name}_image.png"
            img.save(filename)
            print(f"✅ Created: {filename}")

        print(f"\n🎉 All images saved in '{output_dir}' folder!")
        print("📸 Upload these to your Etsy listing in this order:")
        print("1. main_image.png (thumbnail)")
        print("2. whats_included_image.png")
        print("3. preview_image.png")
        print("4. benefits_image.png")
        print("5. instant_download_image.png")

        return output_dir


# Usage with your product data
def main():
    # Load your product data (replace with your JSON file)
    with open('digital_products_20250629_102651.json', 'r') as f:
        data = json.load(f)

    # Use the first product (AI Productivity Planner)
    product_data = data['products'][0]

    # Create image agent
    agent = EtsyImageAgent()

    # Generate all images
    agent.generate_all_images(product_data)


if __name__ == "__main__":
    main()