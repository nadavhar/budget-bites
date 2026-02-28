-- Allow guest posts (no account required)
ALTER TABLE public.feed_posts ALTER COLUMN user_id DROP NOT NULL;

-- Update view to treat null user_id as anonymous
CREATE OR REPLACE VIEW public.public_feed_posts AS
SELECT
  id,
  restaurant_id,
  tip,
  is_anonymous,
  created_at,
  CASE WHEN is_anonymous OR user_id IS NULL THEN NULL ELSE user_id END AS user_id
FROM public.feed_posts;

-- Update INSERT policy to allow unauthenticated inserts
-- (Edge Function uses service role key anyway, so this is a safety fallback)
DROP POLICY IF EXISTS "feed_posts_insert_own" ON public.feed_posts;
CREATE POLICY "feed_posts_insert_all" ON public.feed_posts
  FOR INSERT WITH CHECK (true);
