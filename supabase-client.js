/**
 * EVENTWEB — Supabase Backend Client Module
 * Provides real-time event discovery, registrations, organizer auth, and poster storage.
 */

// 1. Supabase Project Credentials
const SUPABASE_CONFIG = {
  url: window.__EW_SUPABASE_URL || 'https://zjedibwbzxqjudxyhuyi.supabase.co',
  anonKey: window.__EW_SUPABASE_ANON_KEY || 'sb_publishable_NaRHL9Nz6IM8E7eWPTqdgA_SU8Yyr4e'
};

// Check if credentials have been configured
const isSupabaseConfigured = () => {
  return SUPABASE_CONFIG.url &&
    !SUPABASE_CONFIG.url.includes('YOUR_PROJECT_ID') &&
    SUPABASE_CONFIG.anonKey &&
    !SUPABASE_CONFIG.anonKey.includes('YOUR_ANON_KEY');
};

let supabase = null;

if (typeof window !== 'undefined' && window.supabase && isSupabaseConfigured()) {
  supabase = window.supabase.createClient(SUPABASE_CONFIG.url, SUPABASE_CONFIG.anonKey);
}

// 2. Events API
export const EventService = {
  // Fetch all published events
  async getEvents() {
    if (!supabase) return null;
    try {
      const { data, error } = await supabase
        .from('events')
        .select('*')
        .eq('status', 'published')
        .order('date', { ascending: true });

      if (error) throw error;
      return data;
    } catch (err) {
      console.warn('Supabase fetch events error:', err);
      return null;
    }
  },

  // Create/Publish a new event from Organizer Console
  async createEvent(eventData, posterFile) {
    if (!supabase) throw new Error('Supabase is not configured.');

    let posterUrl = eventData.poster_url || '';

    // Upload poster file if provided
    if (posterFile) {
      const fileExt = posterFile.name.split('.').pop();
      const fileName = `${Date.now()}_${Math.random().toString(36).substring(2, 9)}.${fileExt}`;
      const filePath = `posters/${fileName}`;

      const { error: uploadError } = await supabase.storage
        .from('event-posters')
        .upload(filePath, posterFile);

      if (uploadError) throw uploadError;

      const { data: publicUrlData } = supabase.storage
        .from('event-posters')
        .getPublicUrl(filePath);

      posterUrl = publicUrlData.publicUrl;
    }

    const { data: user } = await supabase.auth.getUser();

    const payload = {
      ...eventData,
      poster_url: posterUrl,
      organizer_id: user?.user?.id || null,
      status: 'published'
    };

    const { data, error } = await supabase
      .from('events')
      .insert([payload])
      .select()
      .single();

    if (error) throw error;
    return data;
  },

  // Register an attendee for an event
  async register(eventId, optionName, attendeeData = {}) {
    const code = 'EW-' + String(Math.floor(1000 + Math.random() * 9000)) + '-' +
      (attendeeData.title || 'EV').replace(/[^a-zA-Z]/g, '').slice(0, 2).toUpperCase();

    if (!supabase) {
      // Local fallback
      return { code, confirmed: true };
    }

    const { data: user } = await supabase.auth.getUser();

    const { data, error } = await supabase
      .from('registrations')
      .insert([{
        event_id: eventId,
        user_id: user?.user?.id || null,
        code,
        option_name: optionName,
        attendee_name: attendeeData.name || null,
        attendee_email: attendeeData.email || null,
        remind_opt_in: attendeeData.remind ?? true
      }])
      .select()
      .single();

    if (error) throw error;
    return data;
  }
};

// 3. Organizer Auth API
export const AuthService = {
  async signUp(email, password, orgName, orgType) {
    if (!supabase) throw new Error('Supabase is not configured.');
    const { data, error } = await supabase.auth.signUp({
      email,
      password,
      options: {
        data: { org_name: orgName, org_type: orgType }
      }
    });
    if (error) throw error;
    return data;
  },

  async signIn(email, password) {
    if (!supabase) throw new Error('Supabase is not configured.');
    const { data, error } = await supabase.auth.signInWithPassword({
      email,
      password
    });
    if (error) throw error;
    return data;
  },

  async signOut() {
    if (!supabase) return;
    const { error } = await supabase.auth.signOut();
    if (error) throw error;
  },

  async getCurrentUser() {
    if (!supabase) return null;
    const { data } = await supabase.auth.getUser();
    return data?.user || null;
  }
};

window.EW_Supabase = {
  isConfigured: isSupabaseConfigured,
  EventService,
  AuthService,
  client: supabase
};
