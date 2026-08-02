"""
Output Schemas

Central place for all AI agent output schemas.
"""


RESEARCH_SCHEMA = {
    "topic": str,
    "summary": str,
    "key_points": list,
    "facts": list,
    "sources": list,
}


SEO_SCHEMA = {
    "titles": list,
    "description": str,
    "tags": list,
    "keywords": list,
    "thumbnail_text": list,
    "viral_score": int,
    "competition": str,
    "best_video_length": str,
    "target_audience": str,
}


TITLE_RANK_SCHEMA = {
    "winner": str,
    "reason": str,
    "rankings": list,
}


HOOK_SCHEMA = {
    "hooks": list,
}


THUMBNAIL_SCHEMA = {
    "thumbnail_title": str,
    "thumbnail_text": list,
    "thumbnail_concept": str,
    "emotion": str,
    "colors": str,
    "subject_focus": str,
}


SCRIPT_SCHEMA = {
    "title": str,
    "hook": str,
    "intro": str,
    "sections": list,
    "cta": str,
    "estimated_duration": str,
}