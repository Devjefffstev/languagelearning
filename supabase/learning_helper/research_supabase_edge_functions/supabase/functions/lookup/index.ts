// Reference Edge Function for the `lookup` function.
// 1. Set the secret first:
//      supabase secrets set SUPABASE_SERVICE_ROLE_KEY=<your service_role key>
// 2. Drop this at supabase/functions/lookup/index.ts
//      (after `supabase functions new lookup`)
// 3. Deploy: supabase functions deploy lookup
// 4. Call: supabase.functions.invoke("lookup", {"body": {"word": "hola"}})

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
