// Edge Function starter — drop this at supabase/functions/greet/index.ts
// (replace the file scaffolded by `supabase functions new greet`).
// Deploy with: supabase functions deploy greet
// Prereq:  supabase secrets set SUPABASE_SERVICE_ROLE_KEY=<key>

import { createClient } from 'npm:@supabase/supabase-js@2'

// TODO 1: Build an admin Supabase client.
//   Use createClient(Deno.env.get('SUPABASE_URL'), Deno.env.get('SUPABASE_SERVICE_ROLE_KEY'))
//   Store it in a const named `admin`.

Deno.serve(async (req) => {
  // TODO 2: Read `word` from `await req.json()`.

  // TODO 3: Query the `words` table for that word:
  //   await admin.from('words').select('word, translation, language')
  //            .eq('word', word).maybeSingle()
  //   Store the row in `data`.

  // TODO 4: Return { found: !!data, word, ...(data ?? {}) } with Response.json(...).
})