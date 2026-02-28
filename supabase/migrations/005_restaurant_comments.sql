-- ============================================================
-- Restaurant Comments (replaces feed-based comments)
-- Comments are now attached directly to a restaurant_id
-- ============================================================
CREATE TABLE IF NOT EXISTS public.restaurant_comments (
  id            UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  restaurant_id TEXT NOT NULL,
  user_id       UUID REFERENCES auth.users(id) ON DELETE SET NULL,
  message       TEXT NOT NULL CHECK (char_length(message) <= 300),
  created_at    TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS restaurant_comments_rid_idx
  ON public.restaurant_comments (restaurant_id, created_at);

-- Public view — strips user_id; everyone is anonymous in chat
CREATE OR REPLACE VIEW public.public_restaurant_comments AS
SELECT id, restaurant_id, message, created_at
FROM public.restaurant_comments;

-- ============================================================
-- RLS
-- ============================================================
ALTER TABLE public.restaurant_comments ENABLE ROW LEVEL SECURITY;

CREATE POLICY "restaurant_comments_select_all" ON public.restaurant_comments FOR SELECT USING (true);
CREATE POLICY "restaurant_comments_insert_all" ON public.restaurant_comments FOR INSERT WITH CHECK (true);

GRANT SELECT ON public.public_restaurant_comments TO anon, authenticated;

-- ============================================================
-- Enable Realtime
-- ============================================================
ALTER PUBLICATION supabase_realtime ADD TABLE public.restaurant_comments;
