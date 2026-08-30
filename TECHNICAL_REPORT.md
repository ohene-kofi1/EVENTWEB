# TECHNICAL REPORT: EVENTWEB
## A Unified Campus Event Discovery, GIS Mapping, and Ticketing Infrastructure for KNUST

---

**Project Title:** EVENTWEB — Campus Event Discovery & Registration Platform  
**Target Institution:** Kwame Nkrumah University of Science and Technology (KNUST), Kumasi, Ghana  
**Domain:** Web Application Engineering, GIS Spatial Integration, Distributed Backend Architecture  
**Author / Presenter:** Engineering Project Team  
**Date:** Academic Year 2025/2026  

---

## 1. Executive Summary

Campus life at tertiary institutions such as Kwame Nkrumah University of Science and Technology (KNUST) is characterized by a high volume of student-driven and faculty-organized activities—spanning academic conferences, departmental dinners, sports tournaments, religious fellowships, and entrepreneurship summits. Historically, event publicity on campus has suffered from severe fragmentation: promotional posters are scattered across disparate WhatsApp group chats, printed physical flyers pasted over notice boards, and temporary social media stories. This leads to information decay, low student turnouts, poor capacity management, and lack of verified attendee records.

**EVENTWEB** is an institutional-grade, full-stack digital solution engineered to unify campus event publicity into a centralized discovery board, interactive campus GIS map, and automated registration pipeline. Designed with a **Modernist architectural design system** (zero-radius, precision 1px hairlines, high-contrast typography) and powered by **Supabase (PostgreSQL + RLS + Storage)** and **Resend (Transactional Email API)**, EVENTWEB bridges student discovery with verified organizer administration.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           EVENTWEB PLATFORM                             │
├───────────────────────────────────┬─────────────────────────────────────┤
│         STUDENT CLIENT            │          ORGANIZER CONSOLE          │
│ • 5s Auto-Rotating Poster Board   │ • Verified Society Authentication   │
│ • Category Filtering & Search     │ • Flyer Upload (Supabase Storage)   │
│ • Interactive KNUST GIS Map       │ • Capacity & Tier Configuration     │
│ • Instant Registration & Code Gen │ • Real-Time Attendee Tracking       │
└─────────────────┬─────────────────┴──────────────────┬──────────────────┘
                  │                                    │
                  ▼                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                       SUPABASE CLOUD INFRASTRUCTURE                     │
│  ┌──────────────────────┐  ┌──────────────────┐  ┌───────────────────┐  │
│  │ PostgreSQL Database  │  │ Supabase Auth    │  │ Storage Buckets   │  │
│  │ (RLS + Triggers)     │  │ (JWT & Sessions) │  │ (event-posters)   │  │
│  └──────────┬───────────┘  └──────────────────┘  └───────────────────┘  │
│             │                                                           │
│             ▼ Database Webhook                                          │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │ Supabase Edge Function (Deno Runtime) + Resend Email API          │  │
│  │ • Automated Ticket Email with Reference Code & Calendar Details   │  │
│  └───────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Problem Statement & System Objectives

### 2.1 The Challenge
1. **Information Fragmentation:** Students miss high-value events due to unindexed publicity channels.
2. **Venue Ambiguity:** Freshmen and non-resident students struggle to locate specific campus halls, auditoriums, and complex grounds (e.g., Great Hall, Brunei Complex, Paa Joe Stadium).
3. **Capacity & Registration Bottlenecks:** Student societies frequently experience overbooking or unconfirmed attendances with no centralized check-in codes.
4. **Visual Fatigue:** Generic user interfaces fail to convey the dynamic culture and identity of campus societies.

### 2.2 Core Engineering Objectives
- **Single Source of Truth:** Aggregate all campus events into five strict taxonomy categories: *Academic, Social, Sports, Religious, and Business*.
- **Spatial Awareness (GIS):** Provide an interactive campus cartography layer pinning events directly to latitude/longitude coordinates on the KNUST campus.
- **Micro-Interaction & Visual Polish:** Implement a 5-second auto-rotating poster deck with intelligent interaction-pause, dark/light theme switching, and WCAG AA accessibility compliance.
- **Enterprise-Grade Data Integrity:** Utilize PostgreSQL with Row-Level Security (RLS), atomic registration counter triggers, and zero client-side privilege leaks.
- **Automated Communication:** Dispatch transactional email passes with unique alphanumeric verification codes (`EW-XXXX-XX`) via Resend.

---

## 3. Technology Stack & Architectural Decisions

| Layer | Technology | Engineering Rationale |
| :--- | :--- | :--- |
| **Frontend Structure** | HTML5 / Declarative Components (`DCLogic`) | Semantic markup, lightweight runtime, ultra-fast initial page loads without heavy framework overhead. |
| **Design System** | Custom CSS3 (Modernist Tokens) | Zero border-radius styling, 1px hairline rules, curated HSL color ramps, responsive layout grid without CSS framework bloat. |
| **Typography** | Google Fonts (`Archivo`, `Bricolage Grotesque`) | High legibility, distinct editorial identity, optimized tabular numerals for dates and reference codes. |
| **GIS Mapping** | Leaflet.js + OpenStreetMap (OSM) Tiles | Client-side spatial rendering, custom SVG drafting callout pins, isolated z-index stacking context. |
| **Database** | Supabase (PostgreSQL 15) | Relational integrity, custom ENUMs, JSONB attendance tiers, database triggers, and native Row-Level Security. |
| **Authentication** | Supabase Auth (JWT) | Role-based authentication separating public student attendees from verified society organizers. |
| **File Storage** | Supabase Storage (`event-posters`) | CDN-backed image hosting with direct public URL generation and strict write policies. |
| **Email Engine** | Resend API + Supabase Edge Functions | Serverless execution (Deno runtime), high deliverability, branded HTML email templating. |

---

## 4. Frontend Engineering & Design System

### 4.1 Modernist Design Language
The visual identity is based on a modernist Swiss/Bauhaus design philosophy:
- **Zero Border-Radius (`--ew-radius: 0px`):** Every button, card, input, and modal features crisp, sharp corners for a timeless editorial aesthetic.
- **1px Hairline Rules (`--ew-rule: 1px`):** Replaced heavy brutalist borders with precise 1px lines (`--ew-rule-color`), allowing cards, sticky headers, and input fields to blend seamlessly.
- **WCAG AA Contrast Verified:** Text colors (`--ew-text`, `--ew-text-muted`) meet and exceed the 4.5:1 contrast ratio against both light (`#ffffff`) and dark (`#090a0f`) backgrounds.

### 4.2 Hero Poster Deck with Autoplay & User Interaction State Machine
The homepage hero displays a 3D perspective poster stack. The component implements a deterministic state machine:
1. **Autoplay Cycle:** Automatically transitions to the next poster every **5000ms (5 seconds)**.
2. **Interaction Reset:** When a user drags a poster, clicks navigation arrows (`← / →`), or clicks a carousel dot, the timer is cleared and immediately restarted for 5 seconds.
3. **Modal Isolation:** Opening an event registration sheet automatically suspends background rotations to preserve user focus.

```
       [ Idle State ] ──( 5000ms Timer Elapsed )──► [ Next Poster ]
             │                                              │
      User Clicks / Drags                             Timer Restarts
             │                                              │
             ▼                                              ▼
   [ Reset 5s Counter ] ◄───────────────────────────────────┘
```

### 4.3 Interactive GIS Campus Map
The campus map integrates Leaflet.js with customized KNUST geospatial data:
- **Pinned Venues:** Great Hall (`6.67475, -1.57220`), Paa Joe Stadium (`6.67780, -1.56950`), College of Science Auditorium (`6.67350, -1.56650`), Prempeh II Library (`6.67510, -1.57180`), KNUST Church (`6.68508, -1.57270`), and Central Campus (`6.67644, -1.57343`).
- **Architectural Drafting Markers:** Custom SVG callout flags with a 2px coordinate stem and dynamic category color bars that synchronize bi-directionally with event list selection.
- **Stacking Isolation:** Enforces `isolation: isolate` and `z-index: 1` boundaries to prevent Leaflet internal panes from overlapping the sticky navigation bar.

---

## 5. Backend Database Architecture & Security Model

The backend is built on PostgreSQL inside Supabase, utilizing relational schema normalization and strict Row-Level Security.

### 5.1 Database Entity-Relationship Schema

```
 ┌─────────────────────────┐         1:N         ┌─────────────────────────┐
 │       ORGANIZERS        │────────────────────►│         EVENTS          │
 ├─────────────────────────┤                     ├─────────────────────────┤
 │ id (UUID, PK, FK Auth)  │                     │ id (UUID, PK)           │
 │ org_name (TEXT)         │                     │ organizer_id (UUID, FK) │
 │ org_type (TEXT)         │                     │ title (TEXT)            │
 │ email (TEXT)            │                     │ category (ENUM)         │
 │ is_verified (BOOL)      │                     │ venue (TEXT)            │
 │ created_at (TIMESTAMPTZ)│                     │ date (DATE)             │
 └─────────────────────────┘                     │ time (TEXT)             │
                                                 │ capacity (INT)          │
                                                 │ reg_count (INT)         │
                                                 │ poster_url (TEXT)       │
                                                 │ options (JSONB)         │
                                                 │ status (ENUM)           │
                                                 └───────────┬─────────────┘
                                                             │
                                                             │ 1:N
                                                             ▼
                                                 ┌─────────────────────────┐
                                                 │      REGISTRATIONS      │
                                                 ├─────────────────────────┤
                                                 │ id (UUID, PK)           │
                                                 │ event_id (UUID, FK)     │
                                                 │ user_id (UUID, FK Null) │
                                                 │ code (TEXT, Unique)     │
                                                 │ option_name (TEXT)      │
                                                 │ attendee_name (TEXT)    │
                                                 │ attendee_email (TEXT)   │
                                                 │ remind_opt_in (BOOL)    │
                                                 │ created_at (TIMESTAMPTZ)│
                                                 └─────────────────────────┘
```

### 5.2 Real-Time Capacity Trigger
To eliminate race conditions in event registration counts, an atomic PostgreSQL trigger increments `reg_count` on every valid row insertion:

```sql
create or replace function public.handle_new_registration()
returns trigger as $$
begin
  update public.events
  set reg_count = reg_count + 1
  where id = new.event_id;
  return new;
end;
$$ language plpgsql security definer;

create trigger on_registration_created
  after insert on public.registrations
  for each row execute procedure public.handle_new_registration();
```

### 5.3 Row Level Security (RLS) Policies
- **Public Reads:** Unauthenticated users can query published events (`status = 'published'`).
- **Organizer Isolation:** Authenticated organizers can only create, edit, or archive events where `auth.uid() = organizer_id`.
- **Attendee Data Privacy:** Attendee records are accessible exclusively by the registering user or the specific organizing society of that event.

---

## 6. Email Infrastructure (Resend & Edge Functions)

EVENTWEB integrates **Resend** to provide instant confirmation tickets and calendar integration:

```
[ Attendee Registers on Frontend ]
               │
               ▼  (POST /rest/v1/registrations)
[ Supabase PostgreSQL Insert Trigger ]
               │
               ▼  (Database Webhook)
[ Supabase Edge Function (Deno) ]
               │
               ▼  (POST https://api.resend.com/emails)
[ Resend Transactional Engine ]
               │
               ▼
[ Attendee Inbox: HTML Pass with EW-XXXX-XX Code ]
```

### Key Email Features:
1. **Reference Code Generation:** Every ticket is encoded with an alphanumeric code (`EW-4471-KQ`) matching the organizer's door-check roster.
2. **Automated Reminders:** Scheduled notices sent 24 hours and 1 hour prior to event start time.
3. **Security:** API keys are stored exclusively as encrypted environment secrets (`RESEND_API_KEY`) within Supabase Edge compute instances.

---

## 7. Verification & Performance Validation

| Metric | Target / Standard | Result Achieved |
| :--- | :--- | :--- |
| **Visual Styling** | Consistent 1px Hairlines | Verified across Navbar, Cards, Inputs, and Modals |
| **Autoplay Rotation** | 5.0s Cycle with Interaction Reset | Functional with drag, touch, and button controls |
| **Dark Mode Switching** | Zero FOUC (Flash of Unstyled Content) | Handled via `data-theme` attribute in `<head>` |
| **Mobile Responsiveness** | Breakpoints at 900px, 720px, 560px | Stacking layouts without horizontal scroll |
| **GIS Integration** | Real-time pin filtering | Synchronized between venue buttons and Leaflet map |
| **Database Integrity** | Atomic registration counter | Validated with PostgreSQL triggers & RLS policies |

---

## 8. Conclusion & Future Roadmap

**EVENTWEB** addresses a longstanding logistical and communication challenge across KNUST by replacing disorganized publicity with a fast, aesthetically refined, and spatially integrated web platform. The decoupled architecture—combining a Modernist frontend, Supabase cloud data layer, and Resend communication pipeline—ensures scalability, security, and exceptional student engagement.

### Future Enhancements:
- **QR Code Scanning App:** A lightweight PWA for door marshals to scan ticket codes at hall entrances.
- **USSD / SMS Fallback:** Integration with Hubtel/Twilio for students without immediate mobile data.
- **Automated Society Verification:** Institutional integration with KNUST SRC / Dean of Students database for verified badge issuance.

---

*Report prepared and submitted for academic project review.*  
*Repository: `https://github.com/ohene-kofi1/EVENTWEB.git`*
