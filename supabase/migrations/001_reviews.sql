-- ============================================================
-- Profiles (extends auth.users)
-- ============================================================
CREATE TABLE IF NOT EXISTS public.profiles (
  id          UUID REFERENCES auth.users(id) ON DELETE CASCADE PRIMARY KEY,
  username    TEXT,
  created_at  TIMESTAMPTZ DEFAULT NOW()
);

-- Auto-create profile on signup
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO public.profiles (id, username)
  VALUES (NEW.id, NEW.raw_user_meta_data->>'username');
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- ============================================================
-- Reviews
-- ============================================================
CREATE TABLE IF NOT EXISTS public.reviews (
  id             UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  restaurant_id  TEXT NOT NULL,
  user_id        UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
  rating         SMALLINT NOT NULL CHECK (rating BETWEEN 1 AND 5),
  text           TEXT CHECK (char_length(text) <= 150),
  is_anonymous   BOOLEAN DEFAULT TRUE,
  created_at     TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS reviews_restaurant_id_idx ON public.reviews (restaurant_id);
CREATE INDEX IF NOT EXISTS reviews_user_id_idx       ON public.reviews (user_id);

-- ============================================================
-- Public view — strips user_id when anonymous
-- ============================================================
CREATE OR REPLACE VIEW public.public_reviews AS
SELECT
  id,
  restaurant_id,
  rating,
  text,
  is_anonymous,
  created_at,
  CASE WHEN is_anonymous THEN NULL ELSE user_id END AS user_id
FROM public.reviews;

-- ============================================================
-- RLS
-- ============================================================
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.reviews  ENABLE ROW LEVEL SECURITY;

-- profiles: anyone can read, only owner can update
CREATE POLICY "profiles_select" ON public.profiles FOR SELECT USING (true);
CREATE POLICY "profiles_update" ON public.profiles FOR UPDATE USING (auth.uid() = id);

-- reviews: only insert via Edge Function (service role key bypasses RLS)
-- No direct SELECT — use the public_reviews view instead
CREATE POLICY "reviews_insert_own" ON public.reviews
  FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Grant view access to anon and authenticated roles
GRANT SELECT ON public.public_reviews TO anon, authenticated;
GRANT SELECT ON public.profiles       TO anon, authenticated;
