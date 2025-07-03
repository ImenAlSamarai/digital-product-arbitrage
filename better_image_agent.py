# Professional Etsy Image Creation Agent - FIXED VERSION
# Save as: better_image_agent.py

import requests
import json
from PIL import Image, ImageDraw, ImageFont
import textwrap
import os


class ProfessionalEtsyAgent:
    def __init__(self):
        self.image_size = (1000, 1000)
        # Modern color palette
        self.bg_color = (245, 247, 250)  # Light gray
        self.primary = (15, 23, 42)  # Dark navy
        self.accent = (59, 130, 246)  # Blue
        self.green = (16, 185, 129)  # Green
        self.orange = (251, 146, 60)  # Orange

    def get_font(self, size):
        """Get font with fallbacks"""
        font_options = [
            "arial.ttf", "Arial.ttf",
            "/System/Library/Fonts/Arial.ttf",
            "/Windows/Fonts/arial.ttf",
            "DejaVuSans.ttf"
        ]

        for font_path in font_options:
            try:
                return ImageFont.truetype(font_path, size)
            except:
                continue

        # Fallback to default but bigger
        return ImageFont.load_default()

    def add_gradient_bg(self, img):
        """Add subtle gradient background"""
        draw = ImageDraw.Draw(img)
        width, height = img.size

        for y in range(height):
            # Create subtle gradient from light to lighter
            ratio = y / height
            r = int(245 + (255 - 245) * ratio * 0.3)
            g = int(247 + (255 - 247) * ratio * 0.3)
            b = int(250 + (255 - 250) * ratio * 0.3)

            draw.line([(0, y), (width, y)], fill=(r, g, b))

        return img

    def create_main_image(self, product_data):
        """Create eye-catching main image"""
        img = Image.new('RGB', self.image_size, self.bg_color)
        img = self.add_gradient_bg(img)
        draw = ImageDraw.Draw(img)

        # Fonts - MUCH bigger
        title_font = self.get_font(85)
        subtitle_font = self.get_font(45)
        price_font = self.get_font(55)

        # Add decorative elements first
        self.add_modern_decorations(draw)

        # Main title - centered and bold
        title_lines = ["AI-POWERED", "PRODUCTIVITY", "MATRIX"]
        y_start = 200

        for i, line in enumerate(title_lines):
            # Get text dimensions
            bbox = draw.textbbox((0, 0), line, font=title_font)
            text_width = bbox[2] - bbox[0]
            x = (self.image_size[0] - text_width) // 2

            # Add shadow effect
            draw.text((x + 3, y_start + 3), line, fill=(0, 0, 0, 50), font=title_font)
            # Main text
            color = self.primary if i != 1 else self.accent
            draw.text((x, y_start), line, fill=color, font=title_font)
            y_start += 90

        # Subtitle with better positioning
        subtitle = "For High-Performance Entrepreneurs"
        bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
        text_width = bbox[2] - bbox[0]
        x = (self.image_size[0] - text_width) // 2
        draw.text((x, y_start + 40), subtitle, fill=self.primary, font=subtitle_font)

        # Price with badge effect
        price = f"${product_data['opportunity']['price']}"
        self.draw_price_badge(draw, price, 150, 750)

        # Add "INSTANT DOWNLOAD" badge
        self.draw_instant_badge(draw, 600, 750)

        return img

    def draw_price_badge(self, draw, price, x, y):
        """Draw attractive price badge"""
        # Badge background
        badge_width, badge_height = 200, 70
        draw.rounded_rectangle([x, y, x + badge_width, y + badge_height],
                               radius=35, fill=self.green)

        # Price text
        font = self.get_font(40)
        bbox = draw.textbbox((0, 0), price, font=font)
        text_width = bbox[2] - bbox[0]
        text_x = x + (badge_width - text_width) // 2
        text_y = y + 15
        draw.text((text_x, text_y), price, fill=(255, 255, 255), font=font)

    def draw_instant_badge(self, draw, x, y):
        """Draw instant download badge"""
        text = "INSTANT"
        badge_width, badge_height = 180, 50
        draw.rounded_rectangle([x, y, x + badge_width, y + badge_height],
                               radius=25, fill=self.orange)

        font = self.get_font(28)
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_x = x + (badge_width - text_width) // 2
        text_y = y + 12
        draw.text((text_x, text_y), text, fill=(255, 255, 255), font=font)

    def add_modern_decorations(self, draw):
        """Add modern geometric decorations"""
        # Top accent lines
        draw.rectangle([50, 50, 350, 60], fill=self.accent)
        draw.rectangle([650, 50, 950, 60], fill=self.green)

        # Bottom accent lines
        draw.rectangle([50, 940, 350, 950], fill=self.orange)
        draw.rectangle([650, 940, 950, 950], fill=self.accent)

        # Corner elements
        draw.ellipse([80, 80, 130, 130], fill=self.green)
        draw.ellipse([870, 870, 920, 920], fill=self.orange)

    def create_whats_included_image(self, product_data):
        """Create attractive what's included image"""
        img = Image.new('RGB', self.image_size, self.bg_color)
        img = self.add_gradient_bg(img)
        draw = ImageDraw.Draw(img)

        # Title
        title_font = self.get_font(70)
        title = "WHAT'S INCLUDED"
        bbox = draw.textbbox((0, 0), title, font=title_font)
        text_width = bbox[2] - bbox[0]
        x = (self.image_size[0] - text_width) // 2

        # Title with underline
        draw.text((x, 80), title, fill=self.primary, font=title_font)
        draw.rectangle([x, 160, x + text_width, 170], fill=self.accent)

        # Items with checkmarks and better spacing
        items = [
            "Complete AI Integration Guide",
            "ChatGPT Workflow Templates",
            "Task Automation Blueprints",
            "Decision-Making Frameworks",
            "12 Comprehensive Chapters",
            "Bonus Templates & Tools",
            "Instant Digital Download"
        ]

        item_font = self.get_font(38)
        y_pos = 220

        for item in items:
            # Checkmark circle
            draw.ellipse([80, y_pos + 5, 110, y_pos + 35], fill=self.green)
            draw.text((88, y_pos + 8), "✓", fill=(255, 255, 255), font=self.get_font(25))

            # Item text
            draw.text((140, y_pos), item, fill=self.primary, font=item_font)
            y_pos += 65

        return img

    def create_benefits_image(self, product_data):
        """Create benefits image with icons"""
        img = Image.new('RGB', self.image_size, self.bg_color)
        img = self.add_gradient_bg(img)
        draw = ImageDraw.Draw(img)

        # Title
        title_font = self.get_font(55)
        title = "TRANSFORM YOUR PRODUCTIVITY"
        bbox = draw.textbbox((0, 0), title, font=title_font)
        text_width = bbox[2] - bbox[0]
        x = (self.image_size[0] - text_width) // 2
        draw.text((x, 60), title, fill=self.primary, font=title_font)

        # Benefits with emojis and better layout
        benefits = [
            ("🚀", "10x Your Efficiency"),
            ("🤖", "Master AI Tools"),
            ("⏰", "Save 10+ Hours Weekly"),
            ("💰", "Boost Revenue"),
            ("🎯", "Stay Focused"),
            ("✨", "Work Smarter Not Harder")
        ]

        benefit_font = self.get_font(42)
        emoji_font = self.get_font(50)

        y_pos = 200
        for emoji, benefit in benefits:
            # Emoji in circle
            draw.ellipse([70, y_pos, 120, y_pos + 50], fill=self.accent)
            draw.text((80, y_pos + 5), emoji, font=emoji_font)

            # Benefit text
            draw.text((150, y_pos + 8), benefit, fill=self.primary, font=benefit_font)
            y_pos += 80

        return img

    def create_preview_image(self, product_data):
        """Create content preview"""
        img = Image.new('RGB', self.image_size, self.bg_color)
        img = self.add_gradient_bg(img)
        draw = ImageDraw.Draw(img)

        # Title
        title_font = self.get_font(65)
        title = "INSIDE PREVIEW"
        bbox = draw.textbbox((0, 0), title, font=title_font)
        text_width = bbox[2] - bbox[0]
        x = (self.image_size[0] - text_width) // 2
        draw.text((x, 70), title, fill=self.primary, font=title_font)

        # Sample chapters in boxes
        chapters = [
            "Chapter 1: AI Productivity Fundamentals",
            "Chapter 5: Automation Workflows",
            "Chapter 8: Decision Making with AI",
            "Chapter 10: Data-Driven Analytics"
        ]

        chapter_font = self.get_font(32)
        y_pos = 200

        for i, chapter in enumerate(chapters):
            # Chapter box
            box_color = [self.accent, self.green, self.orange, self.primary][i % 4]
            draw.rounded_rectangle([60, y_pos, 940, y_pos + 60],
                                   radius=15, fill=box_color)

            # Chapter text
            draw.text((80, y_pos + 15), chapter, fill=(255, 255, 255), font=chapter_font)
            y_pos += 90

        # Page count
        page_font = self.get_font(45)
        page_text = "50+ Pages of Expert Content"
        bbox = draw.textbbox((0, 0), page_text, font=page_font)
        text_width = bbox[2] - bbox[0]
        x = (self.image_size[0] - text_width) // 2
        draw.text((x, 750), page_text, fill=self.green, font=page_font)

        return img

    def create_instant_download_image(self, product_data):
        """Create download info image"""
        img = Image.new('RGB', self.image_size, self.bg_color)
        img = self.add_gradient_bg(img)
        draw = ImageDraw.Draw(img)

        # Title
        title_font = self.get_font(65)
        title = "INSTANT DOWNLOAD"
        bbox = draw.textbbox((0, 0), title, font=title_font)
        text_width = bbox[2] - bbox[0]
        x = (self.image_size[0] - text_width) // 2
        draw.text((x, 100), title, fill=self.primary, font=title_font)

        # Features in attractive boxes
        features = [
            ("📱", "Works on Any Device"),
            ("📄", "PDF Format"),
            ("⚡", "Immediate Access"),
            ("🔄", "Lifetime Updates"),
            ("💾", "Print Friendly")
        ]

        feature_font = self.get_font(40)
        emoji_font = self.get_font(45)

        y_pos = 250
        for emoji, feature in features:
            # Feature box
            draw.rounded_rectangle([100, y_pos, 900, y_pos + 70],
                                   radius=20, fill=(255, 255, 255))

            # Emoji
            draw.text((130, y_pos + 12), emoji, font=emoji_font)

            # Feature text
            draw.text((200, y_pos + 15), feature, fill=self.primary, font=feature_font)
            y_pos += 90

        return img

    def generate_all_images(self, product_data, output_dir="professional_etsy_images"):
        """Generate all professional images"""
        os.makedirs(output_dir, exist_ok=True)

        print("🎨 Creating professional Etsy images...")

        images = {
            "1_main": self.create_main_image(product_data),
            "2_whats_included": self.create_whats_included_image(product_data),
            "3_preview": self.create_preview_image(product_data),
            "4_benefits": self.create_benefits_image(product_data),
            "5_instant_download": self.create_instant_download_image(product_data)
        }

        for name, img in images.items():
            filename = f"{output_dir}/{name}.png"
            img.save(filename, quality=95)
            print(f"✅ Created: {filename}")

        print(f"\n🎉 Professional images ready in '{output_dir}' folder!")
        print("📸 Upload to Etsy in numerical order (1_main first)")

        return output_dir


# Usage
def main():
    with open('digital_products_20250629_102651.json', 'r') as f:
        data = json.load(f)

    product_data = data['products'][0]
    agent = ProfessionalEtsyAgent()
    agent.generate_all_images(product_data)


if __name__ == "__main__":
    main()