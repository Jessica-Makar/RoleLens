-- ==========================================
-- RoleLens: Analysis Usage Tracking
-- ==========================================

-- Store each accepted resume analysis.
CREATE TABLE public.analysis_usage (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    visitor_id UUID NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Enable Row Level Security.
ALTER TABLE public.analysis_usage ENABLE ROW LEVEL SECURITY;

-- Prevent public and authenticated users from accessing the table directly.
REVOKE ALL ON TABLE public.analysis_usage
FROM PUBLIC, anon, authenticated;


-- ==========================================
-- Daily Usage Limit Function
-- ==========================================

CREATE OR REPLACE FUNCTION public.consume_analysis(
    p_visitor_id UUID
)
RETURNS JSON
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = ''
AS $$
DECLARE
    visitor_count INTEGER;
    daily_count INTEGER;
    today_utc DATE := (NOW() AT TIME ZONE 'UTC')::DATE;
BEGIN
    -- Serialize daily usage checks to prevent concurrent requests
    -- from exceeding the global daily limit.
    PERFORM pg_catalog.pg_advisory_xact_lock(
        pg_catalog.hashtext(today_utc::TEXT)
    );

    -- Count this visitor's analyses today.
    SELECT COUNT(*)::INTEGER
    INTO visitor_count
    FROM public.analysis_usage
    WHERE visitor_id = p_visitor_id
      AND (created_at AT TIME ZONE 'UTC')::DATE = today_utc;

    -- Enforce the per-visitor limit of 2 analyses.
    IF visitor_count >= 2 THEN
        SELECT COUNT(*)::INTEGER
        INTO daily_count
        FROM public.analysis_usage
        WHERE (created_at AT TIME ZONE 'UTC')::DATE = today_utc;

        RETURN json_build_object(
            'allowed', FALSE,
            'reason', 'visitor_limit',
            'visitor_used', visitor_count,
            'daily_used', daily_count
        );
    END IF;

    -- Count all analyses across visitors today.
    SELECT COUNT(*)::INTEGER
    INTO daily_count
    FROM public.analysis_usage
    WHERE (created_at AT TIME ZONE 'UTC')::DATE = today_utc;

    -- Enforce the global limit of 10 analyses.
    IF daily_count >= 10 THEN
        RETURN json_build_object(
            'allowed', FALSE,
            'reason', 'daily_limit',
            'visitor_used', visitor_count,
            'daily_used', daily_count
        );
    END IF;

    -- Record the accepted analysis.
    INSERT INTO public.analysis_usage (visitor_id)
    VALUES (p_visitor_id);

    RETURN json_build_object(
        'allowed', TRUE,
        'visitor_used', visitor_count + 1,
        'daily_used', daily_count + 1
    );
END;
$$;


-- ==========================================
-- Function Permissions
-- ==========================================

-- Only the server-side service role can execute this function.
REVOKE ALL ON FUNCTION public.consume_analysis(UUID)
FROM PUBLIC, anon, authenticated;

GRANT EXECUTE ON FUNCTION public.consume_analysis(UUID)
TO service_role;