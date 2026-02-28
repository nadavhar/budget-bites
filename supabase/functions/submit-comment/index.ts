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

    // Auth is optional — guests can comment too
    let userId: string | null = null
    const authHeader = req.headers.get('Authorization')
    if (authHeader) {
      const token = authHeader.replace('Bearer ', '')
      const { data: { user } } = await supabaseAdmin.auth.getUser(token)
      if (user) userId = user.id
    }

    const { restaurant_id, message } = await req.json()

    if (!restaurant_id || typeof restaurant_id !== 'string') {
      return json({ error: 'Invalid input: restaurant_id is required' }, 400)
    }
    if (!message || typeof message !== 'string' || message.trim().length === 0) {
      return json({ error: 'Invalid input: message is required' }, 400)
    }
    if (message.length > 300) {
      return json({ error: 'Message too long (max 300 chars)' }, 400)
    }

    // Rate limit: max 10 comments per hour (authenticated users only)
    if (userId) {
      const oneHourAgo = new Date(Date.now() - 60 * 60 * 1000).toISOString()
      const { count } = await supabaseAdmin
        .from('restaurant_comments')
        .select('id', { count: 'exact', head: true })
        .eq('user_id', userId)
        .gte('created_at', oneHourAgo)

      if (count && count >= 10) {
        return json({ error: 'rate_limit' }, 429)
      }
    }

    const { data: comment, error: insertError } = await supabaseAdmin
      .from('restaurant_comments')
      .insert({
        restaurant_id,
        user_id: userId,
        message: message.trim().slice(0, 300),
      })
      .select()
      .single()

    if (insertError) throw insertError

    return json({ comment }, 201)

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
