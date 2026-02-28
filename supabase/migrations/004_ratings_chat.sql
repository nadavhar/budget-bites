-- ============================================================
-- Add rating column to feed_posts
-- ============================================================
ALTER TABLE public.feed_posts ADD COLUMN IF NOT EXISTS rating SMALLINT CHECK (rating BETWEEN 1 AND 5);

-- Refresh view to include rating
CREATE OR REPLACE VIEW public.public_feed_posts AS
SELECT
  id,
  restaurant_id,
  tip,
  rating,
  is_anonymous,
  created_at,
  CASE WHEN is_anonymous OR user_id IS NULL THEN NULL ELSE user_id END AS user_id
FROM public.feed_posts;

-- ============================================================
-- Chat / Comments table
-- ============================================================
CREATE TABLE IF NOT EXISTS public.feed_comments (
  id         UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  post_id    UUID REFERENCES public.feed_posts(id) ON DELETE CASCADE NOT NULL,
  user_id    UUID REFERENCES auth.users(id) ON DELETE SET NULL,
  message    TEXT NOT NULL CHECK (char_length(message) <= 300),
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS feed_comments_post_id_idx ON public.feed_comments (post_id, created_at);

-- Public view — strips user_id; everyone is anonymous in chat
CREATE OR REPLACE VIEW public.public_feed_comments AS
SELECT id, post_id, message, created_at
FROM public.feed_comments;

-- ============================================================
-- RLS
-- ============================================================
ALTER TABLE public.feed_comments ENABLE ROW LEVEL SECURITY;

CREATE POLICY "feed_comments_select_all" ON public.feed_comments FOR SELECT USING (true);
CREATE POLICY "feed_comments_insert_all" ON public.feed_comments FOR INSERT WITH CHECK (true);

GRANT SELECT ON public.public_feed_comments TO anon, authenticated;

-- ============================================================
-- Enable Realtime
-- ============================================================
ALTER PUBLICATION supabase_realtime ADD TABLE public.feed_comments;
