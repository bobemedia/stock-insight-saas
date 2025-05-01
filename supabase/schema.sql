-- Run inside Supabase SQL editor
create table profiles (
  id uuid references auth.users not null primary key,
  username text unique,
  created_at timestamptz default now()
);

create table watchlists (
  id uuid default gen_random_uuid() primary key,
  user_id uuid references auth.users on delete cascade,
  name text,
  symbols text[] default '{}',
  created_at timestamptz default now()
);