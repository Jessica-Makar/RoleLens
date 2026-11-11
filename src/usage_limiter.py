
import streamlit as st
from supabase import create_client


VISITOR_DAILY_LIMIT = 2
GLOBAL_DAILY_LIMIT = 10


@st.cache_resource
def get_supabase_client():
    """Create a reusable Supabase client."""

    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["service_role_key"]

    return create_client(url, key)



def consume_analysis(visitor_id):
    """Check usage limits and record an accepted analysis."""

    client = get_supabase_client()

    response = client.rpc(
        "consume_analysis",
        {"p_visitor_id": visitor_id}
    ).execute()

    result = response.data

    if isinstance(result, list):
        result = result[0] if result else {}

    if not isinstance(result, dict):
        raise RuntimeError(
            "Unable to verify analysis usage with Supabase."
        )

    return result
