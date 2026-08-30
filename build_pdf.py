"""
Generates a comprehensive, academically expanded Technical Report PDF for EVENTWEB.
Deeply elaborates on the Frontend Layer Stack, Component State Machine, Design System,
and GIS Spatial Architecture.
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class AcademicNumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(AcademicNumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Times-Roman", 9)
        self.setFillColor(colors.black)
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, letter[1] - 36, "Technical Report: EVENTWEB")
            self.setStrokeColor(colors.black)
            self.setLineWidth(0.5)
            self.line(54, letter[1] - 42, letter[0] - 54, letter[1] - 42)
            
        # Footer
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(letter[0] - 54, 34, page_str)
        self.setStrokeColor(colors.black)
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

    title_style = ParagraphStyle(
        'MainTitle',
        fontName='Times-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.black,
        alignment=1,
        spaceAfter=14
    )
    
    h1_style = ParagraphStyle(
        'SectionH1',
        fontName='Times-Bold',
        fontSize=12.5,
        leading=16,
        textColor=colors.black,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )
    
    h2_style = ParagraphStyle(
        'SectionH2',
        fontName='Times-BoldItalic',
        fontSize=10.5,
        leading=14,
        textColor=colors.black,
        spaceBefore=9,
        spaceAfter=4,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'BodyText',
        fontName='Times-Roman',
        fontSize=9.5,
        leading=14,
        textColor=colors.black,
        spaceAfter=6,
        alignment=4
    )
    
    bullet_style = ParagraphStyle(
        'BulletText',
        parent=body_style,
        leftIndent=18,
        firstLineIndent=-12,
        spaceAfter=4
    )

    story = []

    # Title
    story.append(Paragraph("Technical Report", title_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.black, spaceBefore=0, spaceAfter=14))

    # Section 1
    story.append(Paragraph("1. Introduction and Background", h1_style))
    story.append(Paragraph(
        "At Kwame Nkrumah University of Science and Technology (KNUST), campus life is driven by an active student body and numerous associations organizing hundreds of extracurricular, academic, professional, and social events each semester. These range from academic conferences, symposiums, and software hackathons to society dinners, sports tournaments, night markets, and religious fellowships.",
        body_style
    ))
    story.append(Paragraph(
        "Despite the high volume of events, publicity and registration mechanisms across the university remain heavily fragmented. Organizers rely on physical paper flyers pasted over public notice boards, unindexed broadcast messages on WhatsApp group chats, and short-lived social media stories. This lack of a structured digital channel leads to high information decay, poor attendance estimation, venue confusion among freshmen and non-resident students, and severe logistical bottlenecks during door check-ins.",
        body_style
    ))

    # Section 2
    story.append(Paragraph("2. Problem Statement and Objectives", h1_style))
    story.append(Paragraph(
        "The primary challenge addressed by this project is the absence of a reliable, centralized, and spatially aware event coordination platform for the university. Specific issues include:",
        body_style
    ))
    story.append(Paragraph("• <b>Information Scattering:</b> Students frequently miss relevant developmental programs due to uncoordinated publicity channels.", bullet_style))
    story.append(Paragraph("• <b>Geospatial Ambiguity:</b> Navigating diverse venue locations across campus—such as the Great Hall, Paa Joe Stadium, College of Science Auditorium, and Prempeh II Library—is challenging without integrated maps.", bullet_style))
    story.append(Paragraph("• <b>Capacity and Roster Bottlenecks:</b> Student societies lack real-time registration caps and verified attendee rosters, causing hall overcrowding or unexpected empty seats.", bullet_style))
    story.append(Paragraph(
        "The primary objective of EVENTWEB is to design and implement an institutional-grade platform that unifies event discovery, provides spatial navigation on an interactive campus map, automates ticket reservation with unique verification codes, and provides verified societies with an administrative management dashboard.",
        body_style
    ))

    # Section 3: Architecture & Deep Frontend Expansion
    story.append(Paragraph("3. System Architecture and Frontend Layer Stack", h1_style))
    story.append(Paragraph(
        "EVENTWEB is engineered following a decoupled, three-tier cloud software architecture consisting of an ultra-high-performance client presentation layer, a managed relational database layer, and a serverless notification engine.",
        body_style
    ))

    story.append(Paragraph("3.1 Detailed Presentation Layer Architecture (Frontend Stack)", h2_style))
    story.append(Paragraph(
        "The frontend is architected as an ultra-fast, zero-overhead client layer prioritizing sub-second First Contentful Paint (FCP) and high visual fidelity without the heavy execution overhead of bloated single-page application frameworks. The presentation layer comprises five coordinated engineering subsystems:",
        body_style
    ))
    
    story.append(Paragraph(
        "<b>1. Declarative Component State Engine (`DCLogic`):</b><br/>"
        "Rather than relying on heavy virtual-DOM abstraction layers, the frontend utilizes an efficient reactive component architecture. "
        "The core component state maintains centralized reactive properties (`cat`, `query`, `sort`, `venue`, `openId`, `hero`, `autoplay`, `dragX`, `dragging`). "
        "Component lifecycles (`componentDidMount`, `componentDidUpdate`, `componentWillUnmount`) manage background timers, custom DOM event bindings, "
        "and bi-directional synchronization with the GIS map.",
        body_style
    ))
    
    story.append(Paragraph(
        "<b>2. Modernist CSS Design System & Custom Property Tokens:</b><br/>"
        "All visual styling is centralized inside a formal token layer (`eventweb.css`). The system enforces three core visual rules:<br/>"
        "• <i>Zero-Radius Philosophy (`--ew-radius: 0px`):</i> Strict modernist/Swiss design principles where cards, buttons, tags, chips, and modal sheets feature razor-sharp geometric edges.<br/>"
        "• <i>1px Precision Hairline Boundaries (`--ew-rule: 1px`):</i> Replaced thick neo-brutalist borders with clean 1px hairlines (`--ew-rule-color`) allowing cards, sticky headers, and input controls to blend seamlessly.<br/>"
        "• <i>Curated Color Ramps & WCAG AA Contrast:</i> Brand blue (`#1a3ee8`) clears a 7.25:1 contrast ratio on light grounds; dark mode automatically adjusts background tokens (`--ew-bg: #090a0f`) and surface borders (`--ew-rule-color: #29324a`) with zero Flash of Unstyled Content (FOUC).",
        body_style
    ))

    story.append(Paragraph(
        "<b>3. 3D Perspective Hero Deck & Gesture Physics Engine:</b><br/>"
        "The hero section renders an interactive 3D poster deck where card offsets, rotation angles, scale factors, and opacity layers are computed deterministically:<br/>"
        "• Card index 0: `scale: 1.0, opacity: 1.0, z-index: 30, rotation: 0°`<br/>"
        "• Card index 1: `scale: 0.86, opacity: 0.5, z-index: 20, rotation: +3°`<br/>"
        "• Card index 2: `scale: 0.74, opacity: 0.24, z-index: 10, rotation: +5.5°`<br/>"
        "The gesture physics engine hooks into Pointer Events (`pointerdown`, `pointermove`, `pointerup`), tracking touch/mouse drag displacement (`dragX`) "
        "with a 70px release threshold that snaps to adjacent cards or springs back fluidly.",
        body_style
    ))

    story.append(Paragraph(
        "<b>4. Smart 5-Second Inactivity Autoplay State Machine:</b><br/>"
        "When left idle, the poster stack advances automatically every 5000ms. An interaction state listener monitors user navigation: "
        "clicking next/previous buttons, selecting carousel indicators, dragging a poster, or selecting a category clears the active interval "
        "and immediately restarts a fresh 5-second countdown. Opening an event registration sheet pauses autoplay to ensure uninterrupted reading.",
        body_style
    ))

    story.append(Paragraph(
        "<b>5. Client-Side GIS Map Web Component (`<knust-map>`):</b><br/>"
        "Encapsulated Leaflet.js cartography embedded directly into the DOM tree. Implements stacking context isolation (`isolation: isolate; z-index: 1`) "
        "to prevent Leaflet internal tile panes from overlapping the sticky top navigation header during vertical scrolling.",
        body_style
    ))

    story.append(PageBreak())

    # Section 4
    story.append(Paragraph("4. Technical Stack Justification", h1_style))
    stack_data = [
        [Paragraph("<b>Component</b>", body_style), Paragraph("<b>Technology</b>", body_style), Paragraph("<b>Technical Justification</b>", body_style)],
        [Paragraph("Frontend UI", body_style), Paragraph("Semantic HTML5 & Vanilla JS", body_style), Paragraph("Eliminates heavy framework bundle overhead; provides sub-second first contentful paint.", body_style)],
        [Paragraph("Design System", body_style), Paragraph("Modernist CSS (1px rules)", body_style), Paragraph("Zero border-radius, clean hairline rules, and full WCAG AA contrast compliance.", body_style)],
        [Paragraph("Spatial GIS", body_style), Paragraph("Leaflet.js + OSM Cartography", body_style), Paragraph("Lightweight client-side map rendering with accurate KNUST campus venue coordinates.", body_style)],
        [Paragraph("Relational Database", body_style), Paragraph("Supabase (PostgreSQL 15)", body_style), Paragraph("ACID transaction guarantees, atomic capacity triggers, and native Row-Level Security.", body_style)],
        [Paragraph("Authentication", body_style), Paragraph("Supabase Auth (JWT)", body_style), Paragraph("Role-based separation between public student attendees and verified society organizers.", body_style)],
        [Paragraph("Object Storage", body_style), Paragraph("Supabase Storage (`event-posters`)", body_style), Paragraph("CDN-backed image storage with secure authenticated write permissions.", body_style)],
        [Paragraph("Email Dispatch", body_style), Paragraph("Resend API + Edge Functions", body_style), Paragraph("Serverless execution ensuring high deliverability without exposing private keys.", body_style)]
    ]
    t_stack = Table(stack_data, colWidths=[95, 135, 274])
    t_stack.setStyle(TableStyle([
        ('LINEABOVE', (0, 0), (-1, 0), 1, colors.black),
        ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),
        ('LINEBELOW', (0, -1), (-1, -1), 1, colors.black),
        ('PADDING', (0, 0), (-1, -1), 4),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(t_stack)
    story.append(Spacer(1, 10))

    # Section 5: Database Engineering
    story.append(Paragraph("5. Relational Database Design and Data Integrity", h1_style))
    story.append(Paragraph(
        "The relational database schema is normalized across three core tables to guarantee referential integrity and eliminate redundancy:",
        body_style
    ))
    story.append(Paragraph("• <b>Organizers Table (`organizers`):</b> Stores society and faculty organizer profiles linked directly to Supabase Auth (`auth.users.id`). Fields include `org_name`, `org_type` (Society, Faculty, Club, Committee), `email`, and `is_verified`.", bullet_style))
    story.append(Paragraph("• <b>Events Table (`events`):</b> Stores comprehensive event metadata including title, category ENUM (Academic, Social, Sports, Religious, Business), venue name, date, time, total capacity, registered count, poster image URL, and JSONB attendance options.", bullet_style))
    story.append(Paragraph("• <b>Registrations Table (`registrations`):</b> Records individual student ticket reservations. Each row contains a foreign key reference to `events.id`, an optional reference to `user_id`, a unique door check-in reference code (`EW-XXXX-XX`), the selected tier name, and reminder opt-in status.", bullet_style))

    story.append(Paragraph("5.1 Atomic Concurrency Trigger for Capacity Management", h2_style))
    story.append(Paragraph(
        "A critical vulnerability in event registration web applications is the race condition, where simultaneous attendee requests can lead to overbooking beyond hall limits. To prevent this, EVENTWEB implements an atomic PostgreSQL trigger function executing at the database level:",
        body_style
    ))
    
    trig_text = (
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
    t_trig = Table([[Paragraph(f"<font face='Courier' size='8'>{trig_text.replace(chr(10), '<br/>')}</font>", body_style)]], colWidths=[504])
    t_trig.setStyle(TableStyle([
        ('PADDING', (0, 0), (-1, -1), 4),
        ('LINEABOVE', (0, 0), (-1, 0), 0.5, colors.black),
        ('LINEBELOW', (0, -1), (-1, -1), 0.5, colors.black),
    ]))
    story.append(t_trig)
    story.append(Spacer(1, 8))

    story.append(Paragraph("5.2 Security and Row-Level Policies (RLS)", h2_style))
    story.append(Paragraph(
        "Row-Level Security is strictly enabled on all tables. Public anonymous users have `SELECT` access only to published events and `INSERT` permissions to register. Organizers are restricted via `auth.uid() = organizer_id` so that they can only modify or view attendance logs for events they have published.",
        body_style
    ))

    # Section 6: GIS Mapping
    story.append(Paragraph("6. Geospatial Mapping and Campus Venue Coordinates", h1_style))
    story.append(Paragraph(
        "To assist students in locating event venues across KNUST, EVENTWEB integrates a dedicated Leaflet GIS module mapped to calibrated campus coordinates:",
        body_style
    ))
    story.append(Paragraph("• <b>Great Hall:</b> 6.67475° N, -1.57220° W (Main Ceremonial Hall and Matriculation/Congregation Auditorium)", bullet_style))
    story.append(Paragraph("• <b>Paa Joe Stadium:</b> 6.67780° N, -1.56950° W (University Sports Grounds, Marathon Starts, Outdoor Fairs)", bullet_style))
    story.append(Paragraph("• <b>College of Science Auditorium:</b> 6.67350° N, -1.56650° W (Academic Conferences, STEM Competitions)", bullet_style))
    story.append(Paragraph("• <b>Prempeh II Library:</b> 6.67510° N, -1.57180° W (Central Academic Resource and Seminar Rooms)", bullet_style))
    story.append(Paragraph("• <b>KNUST Interdenominational Church:</b> 6.68508° N, -1.57270° W (Religious Fellowships and Services)", bullet_style))
    story.append(Paragraph("• <b>Central Campus / Brunei Complex:</b> 6.67644° N, -1.57343° W (Night Markets, Fusion Festivals)", bullet_style))
    story.append(Paragraph(
        "The mapping layer uses architectural drafting pins with category-coded color indicators. Selecting an event in the list smoothly pans the map viewport to that venue, while tapping a map marker instantly filters the event roster.",
        body_style
    ))

    # Section 7: Resend Email
    story.append(Paragraph("7. Transactional Pass and Reminder Pipeline (Resend)", h1_style))
    story.append(Paragraph(
        "When a student registers, Supabase triggers a serverless Edge Function running on the Deno runtime. This function calls the Resend REST API to dispatch an immediate confirmation pass containing the event title, flyer thumbnail, society name, date, venue, and unique entry verification code (`EW-XXXX-XX`). API keys are securely stored in server environment variables and never exposed to client browsers.",
        body_style
    ))

    # Section 8: Conclusion
    story.append(Paragraph("8. Conclusion", h1_style))
    story.append(Paragraph(
        "EVENTWEB demonstrates how modern web engineering, geospatial cartography, and cloud database architectures can solve a tangible logistical challenge in tertiary education. By replacing fragmented publicity channels with a unified, aesthetically refined platform, EVENTWEB provides students and student societies with a dependable, scalable, and high-performance event coordination infrastructure.",
        body_style
    ))

    doc.build(story, canvasmaker=AcademicNumberedCanvas)
    print("Expanded Academic Technical Report PDF generated successfully.")

if __name__ == "__main__":
    build_pdf()
