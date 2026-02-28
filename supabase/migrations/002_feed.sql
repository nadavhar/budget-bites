-- ============================================================
-- Feed Posts
-- ============================================================
CREATE TABLE IF NOT EXISTS public.feed_posts (
  id             UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id        UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
  restaurant_id  TEXT NOT NULL,
  tip            TEXT CHECK (char_length(tip) <= 150),
  is_anonymous   BOOLEAN DEFAULT TRUE,
  created_at     TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS feed_posts_created_at_idx ON public.feed_posts (created_at DESC);

-- ============================================================
-- Public view — strips user_id when anonymous
-- ============================================================
CREATE OR REPLACE VIEW public.public_feed_posts AS
SELECT
  id,
  restaurant_id,
  tip,
  is_anonymous,
  created_at,
  CASE WHEN is_anonymous THEN NULL ELSE user_id END AS user_id
FROM public.feed_posts;

-- ============================================================
-- RLS
-- ============================================================
ALTER TABLE public.feed_posts ENABLE ROW LEVEL SECURITY;

-- Anyone can read (needed for Realtime subscription payloads)
CREATE POLICY "feed_posts_select_all" ON public.feed_posts
  FOR SELECT USING (true);

-- Only the owning user can insert (Edge Function uses service role, bypasses RLS)
CREATE POLICY "feed_posts_insert_own" ON public.feed_posts
  FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Grant view access to anon and authenticated roles
GRANT SELECT ON public.public_feed_posts TO anon, authenticated;

-- ============================================================
-- Enable Realtime for this table
-- ============================================================
ALTER PUBLICATION supabase_realtime ADD TABLE public.feed_posts;
