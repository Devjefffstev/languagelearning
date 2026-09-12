-- Exercise 03: the Postgres function you'll call from Python with .rpc().
-- (If you already ran examples/setup_complete.sql, this is the same
-- function — running it again is harmless.)

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

-- Make the function callable with the anon API key.
grant execute on function public.word_stats() to anon;
