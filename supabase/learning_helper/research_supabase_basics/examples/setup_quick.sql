-- Quick setup: create the `words` table and let the anon API key
-- read and insert rows. Run this in the Supabase dashboard SQL Editor first.

create table if not exists public.words (
  id bigint generated always as identity primary key,
  word text not null unique,
  translation text not null,
  language text not null,
  created_at timestamptz not null default now()
);

-- Row Level Security: with RLS enabled and no policy, nobody can read or
-- write through the API. Grants + policies are the "house rules".
alter table public.words enable row level security;

-- Grants decide WHICH operations a role may attempt at all.
revoke all on table public.words from anon, authenticated;
grant select, insert on table public.words to anon;

-- Policies decide WHICH ROWS the operation applies to.
-- (Wide open on purpose — this is a learning sandbox, not production.)
create policy "words_select_anon" on public.words for select to anon using (true);
create policy "words_insert_anon" on public.words for insert to anon with check (true);
