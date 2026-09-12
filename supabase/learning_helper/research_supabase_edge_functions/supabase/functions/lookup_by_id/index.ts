// Reference Edge Function — lookup a word by its primary key id.
// 1. Drop this at supabase/functions/lookup_by_id/index.ts
//      (after `supabase functions new lookup_by_id`)
// 2. Deploy: supabase functions deploy lookup_by_id
// 3. Call: supabase.functions.invoke("lookup_by_id", {"body": {"id": 1}})

import { createClient } from 'npm:@supabase/supabase-js@2'

Deno.serve(async (req) => {
  const { id } = await req.json()
  const admin = createClient(
    Deno.env.get('SUPABASE_URL')!,
    Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!,
  )
  const { data } = await admin
    .from('words')
    .select('id, word, translation, language, learned')
    .eq('id', id)
    .maybeSingle()
  return Response.json({ found: !!data, id, ...(data ?? {}) })
})
