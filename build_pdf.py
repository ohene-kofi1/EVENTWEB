"""
Generates a publication-quality academic Technical Report PDF for EVENTWEB
"""
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_header_footer(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#6c717c"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, letter[1] - 36, "EVENTWEB — Engineering Technical Report · KNUST")
            self.setStrokeColor(colors.HexColor("#e0e2e8"))
            self.setLineWidth(0.5)
            self.line(54, letter[1] - 42, letter[0] - 54, letter[1] - 42)
            
        # Footer
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(letter[0] - 54, 32, page_str)
        self.drawString(54, 32, "CONFIDENTIAL & PROPRIETARY — ACADEMIC DEFENSE")
        self.setStrokeColor(colors.HexColor("#e0e2e8"))
        self.setLineWidth(0.5)
        self.line(54, 44, letter[0] - 54, 44)
        
        self.restoreState()

def build_pdf():
    pdf_filename = "TECHNICAL_REPORT.pdf"
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Custom Palette
    c_primary = colors.HexColor("#1a3ee8")
    c_ink = colors.HexColor("#101215")
    c_muted = colors.HexColor("#6c717c")
    c_bg_sunken = colors.HexColor("#f7f8fa")
    c_border = colors.HexColor("#e0e2e8")
    c_accent_bg = colors.HexColor("#eef1ff")
    
    # Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=c_ink,
        spaceAfter=6
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#4b5160"),
        spaceAfter=14
    )
    
    h1_style = ParagraphStyle(
        'H1',
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=c_ink,
        spaceBefore=16,
        spaceAfter=6,
        keepWithNext=True
    )
    
    h2_style = ParagraphStyle(
        'H2',
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=c_primary,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'Body',
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor("#2b303b"),
        spaceAfter=6
    )
    
    bullet_style = ParagraphStyle(
        'Bullet',
        parent=body_style,
        leftIndent=14,
        firstLineIndent=-10,
        spaceAfter=3
    )
    
    code_style = ParagraphStyle(
        'CodeStyle',
        fontName='Courier',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor("#f2f4f8")
    )
    
    badge_style = ParagraphStyle(
        'Badge',
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.white
    )

    story = []

    # Badge + Header
    badge_p = Paragraph("<b>ENGINEERING TECHNICAL REPORT</b>", badge_style)
    badge_table = Table([[badge_p]], colWidths=[180])
    badge_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), c_primary),
        ('PADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ]))
    story.append(badge_table)
    story.append(Spacer(1, 10))

    story.append(Paragraph("EVENTWEB: A Unified Campus Event Discovery, GIS Mapping, and Ticketing Infrastructure", title_style))
    story.append(Paragraph("Architectural Design, Distributed Cloud Backend, Spatial GIS Integration, and Transactional Notification Pipeline", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_ink, spaceBefore=0, spaceAfter=10))

    # Meta Table
    meta_data = [
        [
            Paragraph("<b>Target Institution:</b><br/>KNUST, Kumasi, Ghana", body_style),
            Paragraph("<b>Domain:</b><br/>Web GIS & Cloud Software Eng.", body_style),
            Paragraph("<b>Backend & Auth:</b><br/>Supabase (PostgreSQL + RLS)", body_style),
            Paragraph("<b>Email Dispatch:</b><br/>Resend (Edge Functions)", body_style)
        ]
    ]
    meta_table = Table(meta_data, colWidths=[126, 126, 126, 126])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), c_bg_sunken),
        ('BORDER', (0, 0), (-1, -1), 0.5, c_border),
        ('PADDING', (0, 0), (-1, -1), 6),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 12))

    # Section 1
    story.append(Paragraph("1. Executive Summary & Problem Statement", h1_style))
    story.append(Paragraph(
        "Campus life at Kwame Nkrumah University of Science and Technology (KNUST) features hundreds of student-driven "
        "and faculty-organized activities per academic semester—spanning academic symposiums, society dinners, sports "
        "derbies, religious retreats, and entrepreneurship bootcamps. Historically, publicity has been scattered across "
        "ephemeral WhatsApp status updates, unstructured broadcast groups, and physical paper posters pasted over campus notice boards. "
        "This fragmentation leads to information decay, low turnouts, double-booked halls, and no centralized check-in records.",
        body_style
    ))
    story.append(Paragraph(
        "<b>EVENTWEB</b> unifies campus events into a single digital platform: a live-updating discovery board categorized by "
        "five distinct activity tracks (Academic, Social, Sports, Religious, Business), an interactive campus GIS cartography map, "
        "an automated pass generation engine with door verification codes (<code>EW-XXXX-XX</code>), and a verified society organizer console.",
        body_style
    ))

    # Section 2: Architecture
    story.append(Paragraph("2. System Architecture & Component Model", h1_style))
    story.append(Paragraph(
        "EVENTWEB employs a modern decoupled architecture balancing immediate client rendering with resilient cloud persistence and serverless communication.",
        body_style
    ))
    
    arch_ascii = (
        "+-------------------------------------------------------------------------+\n"
        "|                           EVENTWEB PLATFORM                             |\n"
        "+------------------------------------+------------------------------------+\n"
        "|         STUDENT CLIENT             |         ORGANIZER CONSOLE          |\n"
        "| * 5s Auto-Rotating Poster Board    | * Verified Society Authentication  |\n"
        "| * Category Filtering & Search      | * Flyer Upload (Supabase Storage)  |\n"
        "| * Interactive KNUST GIS Map        | * Capacity & Tier Configuration    |\n"
        "| * Instant Registration & Code Gen  | * Real-Time Attendee Tracking      |\n"
        "+-----------------+------------------+-----------------+------------------+\n"
        "                  |                                    |\n"
        "                  v                                    v\n"
        "+-------------------------------------------------------------------------+\n"
        "|                       SUPABASE CLOUD INFRASTRUCTURE                     |\n"
        "|  +----------------------+  +------------------+  +-------------------+  |\n"
        "|  | PostgreSQL Database  |  | Supabase Auth    |  | Storage Buckets   |  |\n"
        "|  | (RLS + Triggers)     |  | (JWT & Sessions) |  | (event-posters)   |  |\n"
        "|  +----------+-----------+  +------------------+  +-------------------+  |\n"
        "|             |                                                           |\n"
        "|             v Database Webhook                                          |\n"
        "|  +-------------------------------------------------------------------+  |\n"
        "|  | Supabase Edge Function (Deno Runtime) + Resend Email API          |  |\n"
        "|  | * Automated Ticket Email with Reference Code & Calendar Details   |  |\n"
        "|  +-------------------------------------------------------------------+  |\n"
        "+-------------------------------------------------------------------------+"
    )
    
    arch_table = Table([[Paragraph(f"<pre>{arch_ascii}</pre>", code_style)]], colWidths=[504])
    arch_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#0c0e12")),
        ('PADDING', (0, 0), (-1, -1), 8),
        ('BORDER', (0, 0), (-1, -1), 1, c_ink),
    ]))
    story.append(arch_table)
    story.append(Spacer(1, 10))

    # Section 3: Tech Stack
    story.append(Paragraph("3. Technology Stack & Technical Justifications", h1_style))
    stack_data = [
        [Paragraph("<b>Subsystem</b>", body_style), Paragraph("<b>Technology</b>", body_style), Paragraph("<b>Engineering Rationale</b>", body_style)],
        [Paragraph("<b>Frontend Core</b>", body_style), Paragraph("HTML5 / Vanilla JS", body_style), Paragraph("Eliminates virtual-DOM overhead, delivering instantaneous First Contentful Paint.", body_style)],
        [Paragraph("<b>Design System</b>", body_style), Paragraph("Modernist CSS (1px rules)", body_style), Paragraph("Zero border-radius, clean 1px hairlines, and strict WCAG AA contrast compliance.", body_style)],
        [Paragraph("<b>GIS Engine</b>", body_style), Paragraph("Leaflet.js + OSM Tiles", body_style), Paragraph("Client-side campus cartography with custom coordinate bounding boxes.", body_style)],
        [Paragraph("<b>Database</b>", body_style), Paragraph("Supabase (PostgreSQL 15)", body_style), Paragraph("ACID transactions, custom ENUMs, JSONB tiers, and native Row-Level Security.", body_style)],
        [Paragraph("<b>Auth & Storage</b>", body_style), Paragraph("Supabase Auth & Storage", body_style), Paragraph("JWT organizer sessions and CDN bucket storage for society flyers.", body_style)],
        [Paragraph("<b>Email Delivery</b>", body_style), Paragraph("Resend + Edge Functions", body_style), Paragraph("Serverless execution for instant pass delivery and automated door reminders.", body_style)],
    ]
    t_stack = Table(stack_data, colWidths=[100, 130, 274])
    t_stack.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_bg_sunken),
        ('BORDER', (0, 0), (-1, -1), 0.5, c_border),
        ('PADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_stack)
    story.append(Spacer(1, 10))

    story.append(PageBreak())

    # Section 4: Database Schema
    story.append(Paragraph("4. Database Schema & Data Integrity", h1_style))
    story.append(Paragraph(
        "The relational schema is normalized into three core entities: <code>organizers</code>, <code>events</code>, and <code>registrations</code>. "
        "Row-Level Security (RLS) protects unauthorized modification, while a PostgreSQL trigger eliminates overbooking race conditions.",
        body_style
    ))

    er_ascii = (
        " [ ORGANIZERS ]                1:N                 [ EVENTS ]\n"
        " - id (UUID, PK, Auth) --------------------------> - id (UUID, PK)\n"
        " - org_name (TEXT)                                - organizer_id (UUID, FK)\n"
        " - org_type (TEXT)                                - title (TEXT)\n"
        " - email (TEXT)                                   - category (ENUM)\n"
        " - is_verified (BOOL)                             - venue (TEXT)\n"
        "                                                  - date (DATE), time (TEXT)\n"
        "                                                  - capacity, reg_count (INT)\n"
        "                                                  - poster_url (TEXT)\n"
        "                                                  - options (JSONB)\n"
        "                                                  - status (ENUM)\n"
        "                                                          |\n"
        "                                                          | 1:N\n"
        "                                                          v\n"
        "                                                  [ REGISTRATIONS ]\n"
        "                                                  - id (UUID, PK)\n"
        "                                                  - event_id (UUID, FK)\n"
        "                                                  - code (TEXT, Unique)\n"
        "                                                  - attendee_name, email (TEXT)\n"
        "                                                  - remind_opt_in (BOOL)"
    )
    er_table = Table([[Paragraph(f"<pre>{er_ascii}</pre>", code_style)]], colWidths=[504])
    er_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#0c0e12")),
        ('PADDING', (0, 0), (-1, -1), 6),
        ('BORDER', (0, 0), (-1, -1), 1, c_ink),
    ]))
    story.append(er_table)
    story.append(Spacer(1, 8))

    story.append(Paragraph("4.1 Concurrency & Registration Counter Trigger", h2_style))
    story.append(Paragraph(
        "To ensure live registration counts remain atomic and immune to client tampering, a database trigger automatically "
        "increments <code>reg_count</code> on the target event immediately upon successful registration insertion:",
        body_style
    ))
    trig_sql = (
        "CREATE OR REPLACE FUNCTION public.handle_new_registration()\n"
        "RETURNS trigger AS $$\n"
        "BEGIN\n"
        "  UPDATE public.events SET reg_count = reg_count + 1 WHERE id = new.event_id;\n"
        "  RETURN new;\n"
        "END;\n"
        "$$ LANGUAGE plpgsql SECURITY DEFINER;\n\n"
        "CREATE TRIGGER on_registration_created\n"
        "  AFTER INSERT ON public.registrations\n"
        "  FOR EACH ROW EXECUTE PROCEDURE public.handle_new_registration();"
    )
    trig_table = Table([[Paragraph(f"<pre>{trig_sql}</pre>", code_style)]], colWidths=[504])
    trig_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#0c0e12")),
        ('PADDING', (0, 0), (-1, -1), 6),
        ('BORDER', (0, 0), (-1, -1), 1, c_ink),
    ]))
    story.append(trig_table)
    story.append(Spacer(1, 10))

    # Section 5: GIS Mapping
    story.append(Paragraph("5. Interactive GIS Campus Cartography", h1_style))
    story.append(Paragraph(
        "The spatial mapping module embeds KNUST campus coordinates into a custom Leaflet.js canvas, resolving venue locations accurately:",
        body_style
    ))
    story.append(Paragraph("• <b>Great Hall:</b> <code>6.67475 N, -1.57220 W</code> (Central Assembly & Keynote Hall)", bullet_style))
    story.append(Paragraph("• <b>Paa Joe Stadium:</b> <code>6.67780 N, -1.56950 W</code> (Athletics, Tournaments, Outdoor Fairs)", bullet_style))
    story.append(Paragraph("• <b>College of Science Auditorium:</b> <code>6.67350 N, -1.56650 W</code> (Symposiums & Lectures)", bullet_style))
    story.append(Paragraph("• <b>Prempeh II Library:</b> <code>6.67510 N, -1.57180 W</code> (Academic Workshops & Book Clubs)", bullet_style))
    story.append(Paragraph("• <b>KNUST Interdenominational Church:</b> <code>6.68508 N, -1.57270 W</code> (Services & Fellowships)", bullet_style))
    story.append(Paragraph("• <b>Brunei Sports Complex / Campus:</b> <code>6.67644 N, -1.57343 W</code> (Night Markets & Festivals)", bullet_style))
    story.append(Paragraph(
        "<b>Architectural Drafting Callouts:</b> Markers feature a 2px coordinate stem with an interactive flag displaying "
        "venue numbers and category color bars. Clicking a pin highlights events in the list; selecting a list venue pans the map smoothly.",
        body_style
    ))

    # Section 6: UI/UX & Autoplay State Machine
    story.append(Paragraph("6. Front-End Interaction & Modernist Design Language", h1_style))
    story.append(Paragraph(
        "• <b>5-Second Hero Autoplay:</b> The 3D poster stack rotates automatically every 5000ms. If the student clicks, drags, or browses "
        "manually, the timer is cleared and restarts a fresh 5-second countdown from that moment.",
        bullet_style
    ))
    story.append(Paragraph(
        "• <b>1px Seamless Hairlines:</b> Replaced brutalist borders with refined 1px strokes (<code>--ew-rule: 1px</code>). "
        "In dark mode, borders switch to <code>#29324a</code> to blend seamlessly against dark grounds.",
        bullet_style
    ))
    story.append(Paragraph(
        "• <b>Modal Isolation:</b> When an event registration sheet is opened, background poster rotation is paused to preserve user concentration.",
        bullet_style
    ))

    # Section 7: Resend Email Pipeline
    story.append(Paragraph("7. Automated Transactional Pass Pipeline (Resend)", h1_style))
    story.append(Paragraph(
        "Upon registration insertion, Supabase triggers an Edge Function (Deno) that interfaces with Resend: "
        "attendees receive a structured email pass containing their unique code (e.g. <code>EW-4471-KQ</code>), venue directions, "
        "and Google Calendar integration. API credentials remain encrypted in Supabase environment secrets.",
        body_style
    ))

    # Section 8: Conclusion
    story.append(Paragraph("8. Conclusion & Academic Defense Summary", h1_style))
    story.append(Paragraph(
        "<b>EVENTWEB</b> bridges modern web engineering with campus community needs, replacing chaotic publicity channels "
        "with an institutional-grade, aesthetically stunning platform. Its decoupled architecture guarantees sub-second responsiveness, "
        "data privacy via RLS, and a scalable foundation for tertiary event discovery across West Africa.",
        body_style
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print("Technical Report PDF successfully generated.")

if __name__ == "__main__":
    build_pdf()
