import { serve } from "https://deno.land/std@0.168.0/http/server.ts";

const RESEND_API_KEY = Deno.env.get("RESEND_API_KEY");

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
};

serve(async (req) => {
  if (req.method === "OPTIONS") {
    return new Response("ok", { headers: corsHeaders });
  }

  try {
    const { record } = await req.json(); // Triggered by Supabase Database Webhook or direct fetch

    if (!record || !record.attendee_email) {
      return new Response(JSON.stringify({ error: "No attendee email provided" }), {
        status: 400,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    const {
      code,
      attendee_name,
      attendee_email,
      option_name,
      event_title,
      event_date,
      event_time,
      event_venue,
      poster_url,
      organizer_name
    } = record;

    const emailHtml = `
      <!DOCTYPE html>
      <html>
      <head>
        <meta charset="utf-8">
        <style>
          body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #f7f8fa; margin: 0; padding: 24px; color: #101215; }
          .card { max-width: 540px; margin: 0 auto; background: #ffffff; border: 1px solid #101215; border-radius: 0; overflow: hidden; }
          .header { background: #1a3ee8; color: #ffffff; padding: 24px 28px; }
          .brand { font-size: 14px; font-weight: 800; letter-spacing: 0.12em; text-transform: uppercase; margin-bottom: 8px; }
          .title { font-size: 24px; font-weight: 800; line-height: 1.2; margin: 0; }
          .body { padding: 28px; }
          .meta-row { display: flex; justify-content: space-between; border-bottom: 1px solid #e8e9ed; padding: 12px 0; font-size: 14px; }
          .meta-label { color: #6c717c; font-weight: 600; text-transform: uppercase; font-size: 12px; letter-spacing: 0.05em; }
          .meta-value { font-weight: 700; color: #101215; text-align: right; }
          .code-box { background: #0c0e12; color: #ffffff; padding: 20px; text-align: center; margin: 24px 0 16px; border: 1px solid #101215; }
          .code-label { font-size: 11px; font-weight: 700; letter-spacing: 0.14em; color: #9aa0aa; text-transform: uppercase; }
          .code-value { font-size: 28px; font-weight: 900; letter-spacing: 0.05em; font-family: monospace; margin-top: 6px; color: #ffffff; }
          .footer { font-size: 12px; color: #6c717c; text-align: center; padding-top: 16px; }
        </style>
      </head>
      <body>
        <div class="card">
          <div class="header">
            <div class="brand">EVENTWEB · KNUST</div>
            <h1 class="title">${event_title || "Campus Event Registration"}</h1>
          </div>
          <div class="body">
            <p style="margin:0 0 18px;font-size:15px;line-height:1.5;">
              Hello <strong>${attendee_name || "Student"}</strong>, your registration is confirmed! Present this reference code at the door.
            </p>

            <div class="code-box">
              <div class="code-label">YOUR ENTRY REFERENCE CODE</div>
              <div class="code-value">${code}</div>
            </div>

            <div class="meta-row">
              <span class="meta-label">Organizer</span>
              <span class="meta-value">${organizer_name || "Society"}</span>
            </div>
            <div class="meta-row">
              <span class="meta-label">Date & Time</span>
              <span class="meta-value">${event_date || ""} · ${event_time || ""}</span>
            </div>
            <div class="meta-row">
              <span class="meta-label">Venue</span>
              <span class="meta-value">${event_venue || "KNUST Campus"}</span>
            </div>
            <div class="meta-row">
              <span class="meta-label">Pass Type</span>
              <span class="meta-value">${option_name || "General Admission"}</span>
            </div>

            <div class="footer">
              EVENTWEB · KNUST, Kumasi<br>
              Every poster on campus, one board.
            </div>
          </div>
        </div>
      </body>
      </html>
    `;

    // Call Resend REST API
    const res = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${RESEND_API_KEY}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        from: "EVENTWEB <tickets@resend.dev>", // Or your custom verified domain e.g. tickets@eventweb.app
        to: [attendee_email],
        subject: `Your Pass for ${event_title || "Event"} [${code}]`,
        html: emailHtml,
      }),
    });

    const data = await res.json();

    return new Response(JSON.stringify(data), {
      status: res.status,
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  } catch (error) {
    return new Response(JSON.stringify({ error: error.message }), {
      status: 500,
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  }
});
