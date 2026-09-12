// Reference Edge Function — name: `greet`.
// 1. Set the secret once:  supabase secrets set SUPABASE_SERVICE_ROLE_KEY=<key>
// 2. Drop this at supabase/functions/greet/index.ts (after `supabase functions new greet`)
// 3. Deploy: supabase functions deploy greet
// 4. Call:  supabase.functions.invoke("greet", {"body": {"word": "hola"}})

import { createClient } from 'npm:@supabase/supabase-js@2'

Deno.serve(async (req) => {
  const { word } = await req.json()
  const admin = createClient(
    Deno.env.get('SUPABASE_URL')!,
    Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!,
  )
  const { data } = await admin
    .from('words')
    .select('word, translation, language')
    .eq('word', word)
    .maybeSingle()
  return Response.json({ found: !!data, word, ...(data ?? {}) })
})