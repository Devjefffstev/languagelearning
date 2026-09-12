-- Complete setup: rebuild the words table with a richer schema,
-- allow full CRUD for the anon key, and add a word_stats() function.

drop table if exists public.words cascade;

create table public.words (
  id bigint generated always as identity primary key,
  word text not null unique,
  translation text not null,
  language text not null,
  example_sentence text not null default '',
  learned boolean not null default false,
  created_at timestamptz not null default now()
);

alter table public.words enable row level security;

-- Full CRUD grants for the anon key (learning sandbox only — in a real
-- app you would require authenticated users and much tighter policies).
revoke all on table public.words from anon, authenticated;
grant select, insert, update, delete on table public.words to anon;

create policy "words_select_anon" on public.words for select to anon using (true);
create policy "words_insert_anon" on public.words for insert to anon with check (true);
create policy "words_update_anon" on public.words for update to anon using (true) with check (true);
create policy "words_delete_anon" on public.words for delete to anon using (true);

-- A custom Postgres function, callable from Python via supabase.rpc("word_stats")
create or replace function public.word_stats()
returns table (language text, total bigint, learned_count bigint)
language sql
stable
as $$
  select language,
         count(*) as total,
         count(*) filter (where learned) as learned_count
  from public.words
  group by language
  order by language;
$$;

grant execute on function public.word_stats() to anon;
