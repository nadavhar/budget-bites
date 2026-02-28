import { serve } from 'https://deno.land/std@0.168.0/http/server.ts'
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
}

serve(async (req) => {
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders })
  }

  try {
    const supabaseAdmin = createClient(
      Deno.env.get('SUPABASE_URL')!,
      Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!,
    )

    // Auth is optional — guests can post too
    let userId: string | null = null
    const authHeader = req.headers.get('Authorization')
    if (authHeader) {
      const token = authHeader.replace('Bearer ', '')
      const { data: { user } } = await supabaseAdmin.auth.getUser(token)
      if (user) userId = user.id
    }

    const { restaurant_id, tip, is_anonymous } = await req.json()

    if (!restaurant_id) {
      return json({ error: 'Invalid input: restaurant_id is required' }, 400)
    }

    // Rate limit: max 5 posts per hour (authenticated users only — by user_id)
    if (userId) {
      const oneHourAgo = new Date(Date.now() - 60 * 60 * 1000).toISOString()
      const { count } = await supabaseAdmin
        .from('feed_posts')
        .select('id', { count: 'exact', head: true })
        .eq('user_id', userId)
        .gte('created_at', oneHourAgo)

      if (count && count >= 5) {
        return json({ error: 'rate_limit' }, 429)
      }
    }

    const { data: post, error: insertError } = await supabaseAdmin
      .from('feed_posts')
      .insert({
        restaurant_id,
        user_id: userId,
        tip: tip ? String(tip).slice(0, 150) : null,
        // Guests are always anonymous; authenticated users can choose
        is_anonymous: userId ? (is_anonymous ?? true) : true,
      })
      .select()
      .single()

    if (insertError) throw insertError

    return json({ post }, 201)

  } catch (err) {
    return json({ error: err.message }, 500)
  }
})

function json(body: unknown, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { ...corsHeaders, 'Content-Type': 'application/json' },
  })
}
