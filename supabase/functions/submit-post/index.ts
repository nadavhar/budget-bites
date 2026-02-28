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

    // Verify JWT
    const authHeader = req.headers.get('Authorization')
    if (!authHeader) {
      return json({ error: 'Missing authorization' }, 401)
    }

    const token = authHeader.replace('Bearer ', '')
    const { data: { user }, error: userError } = await supabaseAdmin.auth.getUser(token)
    if (userError || !user) {
      return json({ error: 'Unauthorized' }, 401)
    }

    const { restaurant_id, tip, is_anonymous } = await req.json()

    // Validate input
    if (!restaurant_id) {
      return json({ error: 'Invalid input: restaurant_id is required' }, 400)
    }

    // Check: rate limit — max 5 posts per hour
    const oneHourAgo = new Date(Date.now() - 60 * 60 * 1000).toISOString()
    const { count: recentCount } = await supabaseAdmin
      .from('feed_posts')
      .select('id', { count: 'exact', head: true })
      .eq('user_id', user.id)
      .gte('created_at', oneHourAgo)

    if (recentCount && recentCount >= 5) {
      return json({ error: 'rate_limit' }, 429)
    }

    // Insert post using service-role key (bypasses RLS, but we've done our own checks)
    const { data: post, error: insertError } = await supabaseAdmin
      .from('feed_posts')
      .insert({
        restaurant_id,
        user_id: user.id,
        tip: tip ? String(tip).slice(0, 150) : null,
        is_anonymous: is_anonymous ?? true,
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
