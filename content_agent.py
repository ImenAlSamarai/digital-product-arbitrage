# Simple Modern Document Agent - Fixed FPDF version
# Save as: simple_modern_agent.py

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
from datetime import datetime
import os

try:
    from fpdf import FPDF
    from fpdf.enums import XPos, YPos
except ImportError:
    print("Installing FPDF...")
    os.system("pip install fpdf2")
    from fpdf import FPDF
    from fpdf.enums import XPos, YPos


class ModernBusinessReport(FPDF):
    def __init__(self):
        super().__init__(format='A4')
        self.set_auto_page_break(auto=True, margin=15)

        # Modern color palette
        self.colors = {
            'primary_dark': (15, 23, 42),  # #0F172A
            'accent_yellow': (245, 158, 11),  # #F59E0B
            'text_primary': (17, 24, 39),  # #111827
            'text_secondary': (107, 114, 128),  # #6B7280
            'text_light': (156, 163, 175),  # #9CA3AF
            'bg_light': (248, 250, 252),  # #F8FAFC
            'white': (255, 255, 255)  # #FFFFFF
        }

    def set_color_rgb(self, color_name):
        """Set color from our palette"""
        r, g, b = self.colors[color_name]
        self.set_text_color(r, g, b)

    def set_fill_color_rgb(self, color_name):
        """Set fill color from our palette"""
        r, g, b = self.colors[color_name]
        self.set_fill_color(r, g, b)

    def header(self):
        """Page header - only for non-cover pages"""
        if self.page_no() > 1:
            self.set_font('Helvetica', 'B', 8)
            self.set_color_rgb('text_light')
            self.cell(0, 10, 'Strategic Business Report', new_x=XPos.LMARGIN, new_y=YPos.TOP)
            self.cell(0, 10, f'Page {self.page_no()}', new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='R')
            self.ln(5)

    def footer(self):
        """Page footer"""
        if self.page_no() > 1:
            self.set_y(-15)
            self.set_font('Helvetica', 'I', 8)
            self.set_color_rgb('text_light')
            footer_text = f'Confidential Business Strategy | {datetime.now().strftime("%B %Y")}'
            self.cell(0, 10, footer_text, new_x=XPos.LMARGIN, new_y=YPos.TOP, align='C')

    def create_cover_page(self):
        """Create modern cover page"""
        self.add_page()

        # Draw geometric elements
        self.set_fill_color_rgb('accent_yellow')
        # Large circle (top right)
        self.ellipse(150, 20, 60, 60, 'F')

        self.set_fill_color_rgb('primary_dark')
        # Smaller circle (overlapping)
        self.ellipse(170, 50, 35, 35, 'F')

        # Cover content
        self.set_xy(20, 60)

        # Label
        self.set_font('Helvetica', 'B', 12)
        self.set_color_rgb('accent_yellow')
        self.cell(0, 10, 'BUSINESS STRATEGY', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(5)

        # Main title
        self.set_font('Helvetica', 'B', 24)
        self.set_color_rgb('primary_dark')
        self.cell(0, 15, 'Strategic Growth', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.cell(0, 15, 'Framework', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(8)

        # Subtitle
        self.set_font('Helvetica', '', 11)
        self.set_color_rgb('text_secondary')
        subtitle_lines = [
            "Comprehensive analysis and actionable recommendations for",
            "sustainable business growth and market leadership in",
            "competitive landscapes."
        ]

        for line in subtitle_lines:
            self.cell(0, 6, line, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(10)

        # Executive summary box
        self.create_info_box(
            "Executive Summary",
            ["This strategic framework delivers proven methodologies for achieving",
             "sustainable competitive advantage through systematic implementation",
             "of data-driven business optimization strategies."],
            box_type="yellow"
        )

        self.ln(15)

        # Statistics
        self.create_stats_section([
            {'number': '300%', 'label': 'Revenue Growth'},
            {'number': '24hrs', 'label': 'Implementation'},
            {'number': '99.8%', 'label': 'Success Rate'}
        ])

        # Footer
        self.set_y(-30)
        self.set_font('Helvetica', '', 9)
        self.set_color_rgb('text_light')
        footer_text = f'Published {datetime.now().strftime("%B %Y")} | Professional Edition | Confidential'
        self.cell(0, 6, footer_text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    def create_info_box(self, title, content_lines, box_type="default"):
        """Create modern info boxes"""
        current_y = self.get_y()

        # Set colors based on type
        if box_type == "yellow":
            self.set_fill_color(254, 243, 199)  # Light yellow
            border_color = self.colors['accent_yellow']
        elif box_type == "dark":
            self.set_fill_color_rgb('primary_dark')
            border_color = self.colors['accent_yellow']
        else:
            self.set_fill_color_rgb('bg_light')
            border_color = self.colors['accent_yellow']

        # Calculate box height based on content
        box_height = 8 + (len(content_lines) * 4) + 8  # padding + content + padding

        # Draw background box
        self.rect(20, current_y, 170, box_height, 'F')

        # Draw left border
        r, g, b = border_color
        self.set_draw_color(r, g, b)
        self.set_line_width(1.5)
        self.line(20, current_y, 20, current_y + box_height)

        # Add content
        self.set_xy(25, current_y + 3)

        # Title
        self.set_font('Helvetica', 'B', 10)
        if box_type == "dark":
            self.set_color_rgb('white')
        else:
            self.set_color_rgb('primary_dark')
        self.cell(0, 6, title, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        # Content
        self.set_x(25)
        self.set_font('Helvetica', '', 9)
        if box_type == "dark":
            self.set_color_rgb('bg_light')
        else:
            self.set_color_rgb('text_primary')

        # Multi-line content
        for line in content_lines:
            self.cell(0, 4, line, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            self.set_x(25)

        self.set_y(current_y + box_height + 5)

    def create_stats_section(self, stats):
        """Create statistics display - better centered"""
        # Calculate total width and center position
        col_width = 56
        total_width = len(stats) * col_width
        start_x = (210 - total_width) / 2  # Center on A4 width (210mm)

        current_y = self.get_y()

        for i, stat in enumerate(stats):
            x_pos = start_x + (i * col_width)

            # Large number - centered in column
            self.set_xy(x_pos, current_y)
            self.set_font('Helvetica', 'B', 18)
            self.set_color_rgb('accent_yellow')
            self.cell(col_width, 10, stat['number'], new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')

            # Label below - centered in column
            self.set_xy(x_pos, current_y + 12)
            self.set_font('Helvetica', '', 8)
            self.set_color_rgb('text_secondary')
            self.cell(col_width, 6, stat['label'].upper(), new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')

        self.ln(25)

    def create_chapter(self, number, title, subtitle=""):
        """Create chapter page"""
        self.add_page()

        # Chapter number - large
        self.set_font('Helvetica', 'B', 48)
        self.set_color_rgb('accent_yellow')
        self.cell(0, 25, f'{number:02d}', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        # Chapter title
        self.set_font('Helvetica', 'B', 20)
        self.set_color_rgb('primary_dark')
        self.cell(0, 12, title, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        if subtitle:
            self.ln(2)
            self.set_font('Helvetica', '', 11)
            self.set_color_rgb('text_secondary')
            self.cell(0, 8, subtitle, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        self.ln(10)

    def create_section(self, title):
        """Create section heading"""
        # Draw underline
        current_y = self.get_y()
        self.set_font('Helvetica', 'B', 14)
        self.set_color_rgb('primary_dark')

        # Get text width for underline
        text_width = self.get_string_width(title)

        self.cell(0, 10, title, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        # Draw yellow underline
        r, g, b = self.colors['accent_yellow']
        self.set_draw_color(r, g, b)
        self.set_line_width(0.8)
        self.line(20, current_y + 8, 20 + text_width, current_y + 8)

        self.ln(5)

    def add_body_text(self, text_lines, text_type="normal"):
        """Add body text with different styles"""
        if text_type == "lead":
            self.set_font('Helvetica', 'B', 11)
        else:
            self.set_font('Helvetica', '', 10)

        self.set_color_rgb('text_primary')

        # Multi-line text handling
        for line in text_lines:
            if line.strip():
                self.cell(0, 6, line.strip(), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            else:
                self.ln(3)
        self.ln(3)

    def create_modern_table(self, headers, data):
        """Create a modern table - better centered"""
        # Calculate column width to fit page width with margins
        available_width = 170  # Page width minus margins
        col_width = available_width / len(headers)
        row_height = 8

        # Calculate starting position to center table
        table_width = len(headers) * col_width
        start_x = (210 - table_width) / 2

        # Position table
        self.set_x(start_x)

        # Headers
        self.set_font('Helvetica', 'B', 9)
        self.set_fill_color_rgb('primary_dark')
        self.set_color_rgb('white')

        for header in headers:
            self.cell(col_width, row_height, header, 1, new_x=XPos.RIGHT, new_y=YPos.TOP, align='C', fill=True)
        self.ln()

        # Data rows
        self.set_font('Helvetica', '', 9)
        self.set_color_rgb('text_primary')

        for i, row in enumerate(data):
            # Position each row
            self.set_x(start_x)

            # Alternate row colors
            if i % 2 == 0:
                self.set_fill_color(255, 255, 255)  # White
            else:
                self.set_fill_color_rgb('bg_light')  # Light gray

            for j, cell in enumerate(row):
                cell_str = str(cell)
                # Highlight monetary values
                if '


def create_sample_report():
    """Create a sample modern business report"""
    pdf = ModernBusinessReport()

    # Cover page
    pdf.create_cover_page()

    # Chapter 1
    pdf.create_chapter(1, "Market Analysis & Strategic Positioning",
                       "Data-driven insights for competitive advantage and sustainable growth")

    # Executive Overview
    pdf.create_section("Executive Overview")
    pdf.add_body_text([
        "The current market environment presents unprecedented opportunities for",
        "strategic positioning and accelerated growth through systematic implementation",
        "of proven business optimization frameworks."
    ], "lead")

    # Callout box
    pdf.create_info_box(
        "Strategic Insight",
        ["Organizations implementing our comprehensive framework achieve 3.5x faster",
         "growth rates compared to industry benchmarks, with sustained performance",
         "improvements maintained over 24+ month periods."]
    )

    # Performance Metrics
    pdf.create_section("Performance Metrics")
    pdf.add_body_text([
        "Our analysis reveals critical performance indicators that directly correlate",
        "with sustainable business success and market leadership positioning."
    ])

    # Create table
    headers = ["Performance Metric", "Current State", "Target Outcome", "Improvement"]
    data = [
        ["Revenue Growth", "$2.4M annually", "$7.8M annually", "+225%"],
        ["Market Share", "12% regional", "34% regional", "+183%"],
        ["Customer Retention", "78% annually", "96% annually", "+23%"],
        ["Operational Efficiency", "67% capacity", "94% capacity", "+40%"]
    ]

    pdf.create_modern_table(headers, data)

    # Implementation Roadmap
    pdf.create_section("Implementation Roadmap")
    pdf.add_body_text([
        "Our systematic approach ensures measurable progress through clearly defined",
        "phases, each building upon previous achievements while maintaining operational",
        "stability and continuous performance optimization."
    ])

    # Roadmap table
    roadmap_headers = ["Phase", "Duration", "Key Deliverables", "Success Metrics"]
    roadmap_data = [
        ["Discovery", "2-3 weeks", "Comprehensive audit", "Baseline established"],
        ["Strategy Development", "3-4 weeks", "Strategic plan", "Plan approved"],
        ["Implementation", "8-12 weeks", "System deployment", "Metrics improved"],
        ["Optimization", "Ongoing", "Performance tuning", "Targets achieved"]
    ]

    pdf.create_modern_table(roadmap_headers, roadmap_data)

    # Final recommendation
    pdf.create_info_box(
        "Strategic Recommendation",
        ["Successful strategic transformation requires both visionary leadership and",
         "systematic execution. Our framework provides the structure, methodologies,",
         "and tools necessary to achieve sustainable competitive advantage in today's",
         "dynamic business environment."],
        "dark"
    )

    # Save the PDF
    filename = "modern_business_report.pdf"
    pdf.output(filename)

    print(f"✅ Modern business report created: {filename}")
    print("\n🎯 Features included:")
    print("   • Modern typography and color scheme")
    print("   • Geometric design elements")
    print("   • Professional tables with highlighting")
    print("   • Strategic info boxes")
    print("   • Executive-level content presentation")
    print("   • Clean, contemporary layout")

    return filename


class ModernBusinessReportTemplate:
    """Template class for creating custom business reports with the established styling"""

    def __init__(self):
        self.pdf = ModernBusinessReport()

    def create_custom_report(self, title, subtitle, sections, output_filename="custom_report.pdf"):
        """Create a custom report with the established modern styling"""

        # Create cover page
        self.pdf.add_page()

        # Draw geometric elements
        self.pdf.set_fill_color_rgb('accent_yellow')
        self.pdf.ellipse(150, 20, 60, 60, 'F')
        self.pdf.set_fill_color_rgb('primary_dark')
        self.pdf.ellipse(170, 50, 35, 35, 'F')

        # Cover content
        self.pdf.set_xy(20, 60)

        # Label (customizable)
        self.pdf.set_font('Helvetica', 'B', 12)
        self.pdf.set_color_rgb('accent_yellow')
        label = sections.get('cover_label', 'BUSINESS STRATEGY')
        self.pdf.cell(0, 10, label.upper(), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.pdf.ln(5)

        # Main title
        self.pdf.set_font('Helvetica', 'B', 24)
        self.pdf.set_color_rgb('primary_dark')
        title_lines = title.split('\n') if '\n' in title else [title]
        for line in title_lines:
            self.pdf.cell(0, 15, line, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.pdf.ln(8)

        # Subtitle
        self.pdf.set_font('Helvetica', '', 11)
        self.pdf.set_color_rgb('text_secondary')
        if isinstance(subtitle, str):
            subtitle_lines = subtitle.split('\n')
        else:
            subtitle_lines = subtitle

        for line in subtitle_lines:
            self.pdf.cell(0, 6, line, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.pdf.ln(10)

        # Executive summary box (if provided)
        if 'executive_summary' in sections:
            self.pdf.create_info_box(
                "Executive Summary",
                sections['executive_summary'],
                box_type="yellow"
            )
            self.pdf.ln(15)

        # Statistics (if provided)
        if 'stats' in sections:
            self.pdf.create_stats_section(sections['stats'])

        # Footer
        self.pdf.set_y(-30)
        self.pdf.set_font('Helvetica', '', 9)
        self.pdf.set_color_rgb('text_light')
        footer_text = f'Published {datetime.now().strftime("%B %Y")} | Professional Edition | Confidential'
        self.pdf.cell(0, 6, footer_text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        # Content chapters
        for i, chapter in enumerate(sections.get('chapters', []), 1):
            self.pdf.create_chapter(
                i,
                chapter['title'],
                chapter.get('subtitle', '')
            )

            # Add chapter sections
            for section in chapter.get('sections', []):
                section_type = section['type']

                if section_type == 'section_title':
                    self.pdf.create_section(section['content'])

                elif section_type == 'body_text':
                    text_type = section.get('style', 'normal')
                    self.pdf.add_body_text(section['content'], text_type)

                elif section_type == 'info_box':
                    self.pdf.create_info_box(
                        section['title'],
                        section['content'],
                        section.get('box_type', 'default')
                    )

                elif section_type == 'table':
                    self.pdf.create_modern_table(
                        section['headers'],
                        section['data']
                    )

        # Save the PDF
        self.pdf.output(output_filename)
        return output_filename


def create_custom_document_example():
    """Example of how to create custom content with the established styling"""

    template = ModernBusinessReportTemplate()

    # Define your custom content
    custom_content = {
        'cover_label': 'DIGITAL STRATEGY',
        'executive_summary': [
            "This comprehensive digital transformation roadmap provides",
            "actionable frameworks for achieving sustainable competitive",
            "advantage in today's rapidly evolving digital landscape."
        ],
        'stats': [
            {'number': '500%', 'label': 'Digital ROI'},
            {'number': '30 days', 'label': 'Time to Value'},
            {'number': '99.9%', 'label': 'Uptime SLA'}
        ],
        'chapters': [
            {
                'title': 'Digital Transformation Strategy',
                'subtitle': 'Framework for sustainable digital growth and innovation',
                'sections': [
                    {
                        'type': 'section_title',
                        'content': 'Market Opportunity Analysis'
                    },
                    {
                        'type': 'body_text',
                        'content': [
                            "Digital transformation presents unprecedented opportunities for",
                            "organizations to reimagine customer experiences, optimize operations,",
                            "and create new revenue streams through innovative digital solutions."
                        ],
                        'style': 'lead'
                    },
                    {
                        'type': 'info_box',
                        'title': 'Key Insight',
                        'content': [
                            "Companies implementing comprehensive digital strategies achieve",
                            "5x faster growth and 40% higher profitability compared to",
                            "traditional business models within 18 months."
                        ],
                        'box_type': 'default'
                    },
                    {
                        'type': 'table',
                        'headers': ['Digital Initiative', 'Investment', 'ROI Timeline', 'Expected Return'],
                        'data': [
                            ['Cloud Migration', '$250K', '6 months', '+300%'],
                            ['AI Implementation', '$400K', '9 months', '+450%'],
                            ['Process Automation', '$150K', '3 months', '+200%']
                        ]
                    }
                ]
            }
        ]
    }

    filename = template.create_custom_report(
        title="Digital Innovation\nFramework",
        subtitle=[
            "Strategic roadmap for digital transformation and",
            "sustainable competitive advantage in modern markets"
        ],
        sections=custom_content,
        output_filename="custom_digital_strategy.pdf"
    )

    print(f"✅ Custom report created: {filename}")
    return filename


if __name__ == "__main__":
    main() in cell_str or '%' in cell_str:
    self.set_font('Helvetica', 'B', 9)
    self.set_color_rgb('accent_yellow')
else:
    self.set_font('Helvetica', '', 9)
    self.set_color_rgb('text_primary')

align = 'R' if ('


def create_sample_report():
    """Create a sample modern business report"""
    pdf = ModernBusinessReport()

    # Cover page
    pdf.create_cover_page()

    # Chapter 1
    pdf.create_chapter(1, "Market Analysis & Strategic Positioning",
                       "Data-driven insights for competitive advantage and sustainable growth")

    # Executive Overview
    pdf.create_section("Executive Overview")
    pdf.add_body_text([
        "The current market environment presents unprecedented opportunities for",
        "strategic positioning and accelerated growth through systematic implementation",
        "of proven business optimization frameworks."
    ], "lead")

    # Callout box
    pdf.create_info_box(
        "Strategic Insight",
        ["Organizations implementing our comprehensive framework achieve 3.5x faster",
         "growth rates compared to industry benchmarks, with sustained performance",
         "improvements maintained over 24+ month periods."]
    )

    # Performance Metrics
    pdf.create_section("Performance Metrics")
    pdf.add_body_text([
        "Our analysis reveals critical performance indicators that directly correlate",
        "with sustainable business success and market leadership positioning."
    ])

    # Create table
    headers = ["Performance Metric", "Current State", "Target Outcome", "Improvement"]
    data = [
        ["Revenue Growth", "$2.4M annually", "$7.8M annually", "+225%"],
        ["Market Share", "12% regional", "34% regional", "+183%"],
        ["Customer Retention", "78% annually", "96% annually", "+23%"],
        ["Operational Efficiency", "67% capacity", "94% capacity", "+40%"]
    ]

    pdf.create_modern_table(headers, data)

    # Implementation Roadmap
    pdf.create_section("Implementation Roadmap")
    pdf.add_body_text([
        "Our systematic approach ensures measurable progress through clearly defined",
        "phases, each building upon previous achievements while maintaining operational",
        "stability and continuous performance optimization."
    ])

    # Roadmap table
    roadmap_headers = ["Phase", "Duration", "Key Deliverables", "Success Metrics"]
    roadmap_data = [
        ["Discovery", "2-3 weeks", "Comprehensive audit", "Baseline established"],
        ["Strategy Development", "3-4 weeks", "Strategic plan", "Plan approved"],
        ["Implementation", "8-12 weeks", "System deployment", "Metrics improved"],
        ["Optimization", "Ongoing", "Performance tuning", "Targets achieved"]
    ]

    pdf.create_modern_table(roadmap_headers, roadmap_data)

    # Final recommendation
    pdf.create_info_box(
        "Strategic Recommendation",
        ["Successful strategic transformation requires both visionary leadership and",
         "systematic execution. Our framework provides the structure, methodologies,",
         "and tools necessary to achieve sustainable competitive advantage in today's",
         "dynamic business environment."],
        "dark"
    )

    # Save the PDF
    filename = "modern_business_report.pdf"
    pdf.output(filename)

    print(f"✅ Modern business report created: {filename}")
    print("\n🎯 Features included:")
    print("   • Modern typography and color scheme")
    print("   • Geometric design elements")
    print("   • Professional tables with highlighting")
    print("   • Strategic info boxes")
    print("   • Executive-level content presentation")
    print("   • Clean, contemporary layout")

    return filename


def main():
    """Create the sample report and demonstrate custom content creation"""
    print("🚀 Creating modern business report...")
    print("📦 Using FPDF (lightweight, no complex dependencies)")

    # Create the original sample
    filename = create_sample_report()
    print(f"✅ Sample report created: {filename}")

    # Demonstrate custom content creation
    print("\n🎯 Creating custom content example...")
    custom_filename = create_custom_document_example()
    print(f"✅ Custom report created: {custom_filename}")

    print("\n📄 Generated files:")
    print(f"   • {filename} (sample report)")
    print(f"   • {custom_filename} (custom content example)")

    print("\n💡 Ready for your original content!")
    print("   • Improved centering and alignment")
    print("   • Template class for easy custom content")
    print("   • Professional styling maintained")
    print("   • Easy to customize with your content")

    print("\n🔧 To create your own content:")
    print("   1. Use ModernBusinessReportTemplate class")
    print("   2. Define your content structure")
    print("   3. Call create_custom_report() method")
    print("   4. Professional PDF generated automatically!")


if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main() in cell_str or '%' in cell_str) else 'L'
    self.cell(col_width, row_height, cell_str, 1, new_x=XPos.RIGHT, new_y=YPos.TOP, align=align, fill=True)
    self.ln()

    self.ln(8)


def create_sample_report():
    """Create a sample modern business report"""
    pdf = ModernBusinessReport()

    # Cover page
    pdf.create_cover_page()

    # Chapter 1
    pdf.create_chapter(1, "Market Analysis & Strategic Positioning",
                       "Data-driven insights for competitive advantage and sustainable growth")

    # Executive Overview
    pdf.create_section("Executive Overview")
    pdf.add_body_text([
        "The current market environment presents unprecedented opportunities for",
        "strategic positioning and accelerated growth through systematic implementation",
        "of proven business optimization frameworks."
    ], "lead")

    # Callout box
    pdf.create_info_box(
        "Strategic Insight",
        ["Organizations implementing our comprehensive framework achieve 3.5x faster",
         "growth rates compared to industry benchmarks, with sustained performance",
         "improvements maintained over 24+ month periods."]
    )

    # Performance Metrics
    pdf.create_section("Performance Metrics")
    pdf.add_body_text([
        "Our analysis reveals critical performance indicators that directly correlate",
        "with sustainable business success and market leadership positioning."
    ])

    # Create table
    headers = ["Performance Metric", "Current State", "Target Outcome", "Improvement"]
    data = [
        ["Revenue Growth", "$2.4M annually", "$7.8M annually", "+225%"],
        ["Market Share", "12% regional", "34% regional", "+183%"],
        ["Customer Retention", "78% annually", "96% annually", "+23%"],
        ["Operational Efficiency", "67% capacity", "94% capacity", "+40%"]
    ]

    pdf.create_modern_table(headers, data)

    # Implementation Roadmap
    pdf.create_section("Implementation Roadmap")
    pdf.add_body_text([
        "Our systematic approach ensures measurable progress through clearly defined",
        "phases, each building upon previous achievements while maintaining operational",
        "stability and continuous performance optimization."
    ])

    # Roadmap table
    roadmap_headers = ["Phase", "Duration", "Key Deliverables", "Success Metrics"]
    roadmap_data = [
        ["Discovery", "2-3 weeks", "Comprehensive audit", "Baseline established"],
        ["Strategy Development", "3-4 weeks", "Strategic plan", "Plan approved"],
        ["Implementation", "8-12 weeks", "System deployment", "Metrics improved"],
        ["Optimization", "Ongoing", "Performance tuning", "Targets achieved"]
    ]

    pdf.create_modern_table(roadmap_headers, roadmap_data)

    # Final recommendation
    pdf.create_info_box(
        "Strategic Recommendation",
        ["Successful strategic transformation requires both visionary leadership and",
         "systematic execution. Our framework provides the structure, methodologies,",
         "and tools necessary to achieve sustainable competitive advantage in today's",
         "dynamic business environment."],
        "dark"
    )

    # Save the PDF
    filename = "modern_business_report.pdf"
    pdf.output(filename)

    print(f"✅ Modern business report created: {filename}")
    print("\n🎯 Features included:")
    print("   • Modern typography and color scheme")
    print("   • Geometric design elements")
    print("   • Professional tables with highlighting")
    print("   • Strategic info boxes")
    print("   • Executive-level content presentation")
    print("   • Clean, contemporary layout")

    return filename


def main():
    """Create the sample report"""
    print("🚀 Creating modern business report...")
    print("📦 Using FPDF (lightweight, no complex dependencies)")

    filename = create_sample_report()

    print(f"\n📄 Report generated: {filename}")
    print("\n💡 This approach:")
    print("   • Works on all systems (no complex dependencies)")
    print("   • Creates professional-looking PDFs")
    print("   • Easy to customize and extend")
    print("   • Fast and reliable")


if __name__ == "__main__":
    main()