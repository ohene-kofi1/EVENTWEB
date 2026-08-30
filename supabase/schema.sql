-- ============================================================
-- EVENTWEB — Complete Supabase PostgreSQL Schema
-- Run this in your Supabase SQL Editor (https://supabase.com/dashboard/project/_/sql)
-- ============================================================

-- 1. Enable UUID Extension
create extension if not exists "uuid-ossp";

-- 2. Create Custom Types
do $$ begin
  create type event_category as enum ('Academic', 'Social', 'Sports', 'Religious', 'Business');
exception
  when duplicate_object then null;
end $$;

do $$ begin
  create type event_status as enum ('draft', 'pending_review', 'published', 'archived');
exception
  when duplicate_object then null;
end $$;

-- 3. Profiles / Organizers Table
create table if not exists public.organizers (
  id uuid references auth.users on delete cascade primary key,
  org_name text not null,
  org_type text default 'Society',
  email text not null,
  avatar_url text,
  is_verified boolean default false,
  created_at timestamptz default timezone('utc'::text, now()) not null,
  updated_at timestamptz default timezone('utc'::text, now()) not null
);

-- 4. Events Table
create table if not exists public.events (
  id uuid default gen_random_uuid() primary key,
  organizer_id uuid references public.organizers(id) on delete set null,
  organizer_name text not null,
  title text not null,
  category event_category not null default 'Social',
  venue text not null,
  date date not null,
  time text not null,
  capacity integer not null default 100,
  reg_count integer not null default 0,
  soon_days integer default 7,
  poster_url text,
  blurb text,
  when_display text,
  deadline text,
  apply_url text,
  options jsonb not null default '[{"name": "General Admission", "note": "Full event access"}]'::jsonb,
  status event_status not null default 'published',
  created_at timestamptz default timezone('utc'::text, now()) not null,
  updated_at timestamptz default timezone('utc'::text, now()) not null
);

-- 5. Registrations Table
create table if not exists public.registrations (
  id uuid default gen_random_uuid() primary key,
  event_id uuid references public.events(id) on delete cascade not null,
  user_id uuid references auth.users(id) on delete set null,
  code text unique not null,
  option_name text not null default 'General Admission',
  attendee_name text,
  attendee_email text,
  remind_opt_in boolean default true,
  created_at timestamptz default timezone('utc'::text, now()) not null
);

-- 6. Trigger to increment event registration count
create or replace function public.handle_new_registration()
returns trigger as $$
begin
  update public.events
  set reg_count = reg_count + 1
  where id = new.event_id;
  return new;
end;
$$ language plpgsql security definer;

drop trigger if exists on_registration_created on public.registrations;
create trigger on_registration_created
  after insert on public.registrations
  for each row execute procedure public.handle_new_registration();

-- 7. Trigger on auth.users for new organizer signup
create or replace function public.handle_new_user()
returns trigger as $$
begin
  insert into public.organizers (id, org_name, org_type, email, is_verified)
  values (
    new.id,
    coalesce(new.raw_user_meta_data->>'org_name', new.email),
    coalesce(new.raw_user_meta_data->>'org_type', 'Society'),
    new.email,
    true
  )
  on conflict (id) do update
  set email = excluded.email;
  return new;
end;
$$ language plpgsql security definer;

drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created
  after insert on auth.users
  for each row execute procedure public.handle_new_user();

-- 8. Enable Row Level Security (RLS)
alter table public.organizers enable row level security;
alter table public.events enable row level security;
alter table public.registrations enable row level security;

-- 9. RLS Policies
-- Organizers
create policy "Organizers are viewable by everyone" on public.organizers
  for select using (true);

create policy "Users can update own organizer profile" on public.organizers
  for update using (auth.uid() = id);

-- Events
create policy "Published events are viewable by everyone" on public.events
  for select using (status = 'published' or auth.uid() = organizer_id);

create policy "Authenticated organizers can insert events" on public.events
  for insert with check (auth.role() = 'authenticated');

create policy "Organizers can update own events" on public.events
  for update using (auth.uid() = organizer_id);

create policy "Organizers can delete own events" on public.events
  for delete using (auth.uid() = organizer_id);

-- Registrations
create policy "Anyone can register for published events" on public.registrations
  for insert with check (true);

create policy "Users and organizers can view relevant registrations" on public.registrations
  for select using (
    auth.uid() = user_id or
    exists (
      select 1 from public.events
      where events.id = registrations.event_id
      and events.organizer_id = auth.uid()
    )
  );

-- 10. Storage Bucket for Posters
insert into storage.buckets (id, name, public)
values ('event-posters', 'event-posters', true)
on conflict (id) do nothing;

create policy "Poster images are publicly accessible"
  on storage.objects for select
  using (bucket_id = 'event-posters');

create policy "Authenticated users can upload posters"
  on storage.objects for insert
  with check (bucket_id = 'event-posters' and auth.role() = 'authenticated');
