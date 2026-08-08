"""
Output Schemas

Central place for all AI agent output schemas.
"""


RESEARCH_SCHEMA = {
    "topic": str,
    "summary": str,
    "key_points": [str],
    "facts": [str],
    "sources": [str],
}


SEO_SCHEMA = {
    "titles": [str],
    "description": str,
    "tags": [str],
    "keywords": [str],
    "thumbnail_text": [str],
    "viral_score": int,
    "competition": str,
    "best_video_length": str,
    "target_audience": str,
}


TITLE_RANK_SCHEMA = {
    "winner": str,
    "reason": str,
    "rankings": [
        {
            "title": str,
            "CTR Score": int,
            "SEO Score": int,
            "Curiosity Score": int,
            "Strengths": str,
            "Weaknesses": str,
        }
    ],
}


HOOK_SCHEMA = {
    "hooks": [str],
}


THUMBNAIL_SCHEMA = {
    "thumbnail_title": str,
    "thumbnail_text": [str],
    "thumbnail_concept": str,
    "emotion": str,
    "colors": str,
    "subject_focus": str,
}


SCRIPT_SCHEMA = {
    "title": str,
    "hook": str,
    "intro": str,
    "sections": [str],
    "cta": str,
    "estimated_duration": str,
}


REVIEW_SCHEMA = {
    "overall_score": int,
    "strengths": [str],
    "weaknesses": [str],
    "improvements": [str],
    "approved": bool,
    "final_comments": str,
}


DIRECTOR_SCHEMA = {
    "overall_score": int,
    "approved": bool,
    "strengths": [str],
    "weaknesses": [str],
    "improvements": [str],
    "final_title": str,
    "final_hook": str,
    "final_comment": str,
}


SCENE_PLAN_SCHEMA = {
    "scenes": [dict],
}


# --------------------------------------------------
# Single Scene Image Prompt
# Used for scene-by-scene generation
# --------------------------------------------------

SINGLE_IMAGE_PROMPT_SCHEMA = {
    "scene": int,
    "title": str,
    "image_prompt": str,
    "negative_prompt": str,
    "style": str,
    "aspect_ratio": str,
}


# --------------------------------------------------
# Final Image Prompt Collection
# --------------------------------------------------

IMAGE_PROMPT_SCHEMA = {
    "images": [
        {
            "scene": int,
            "title": str,
            "image_prompt": str,
            "negative_prompt": str,
            "style": str,
            "aspect_ratio": str,
        }
    ]
}


# --------------------------------------------------
# Single Scene Video Prompt
# (Future Ready)
# --------------------------------------------------

SINGLE_VIDEO_PROMPT_SCHEMA = {
    "scene": int,
    "title": str,
    "video_prompt": str,
    "duration": str,
    "camera_motion": str,
    "transition": str,
}


# --------------------------------------------------
# Final Video Prompt Collection
# --------------------------------------------------

VIDEO_PROMPT_SCHEMA = {
    "videos": [
        {
            "scene": int,
            "title": str,
            "video_prompt": str,
            "duration": str,
            "camera_motion": str,
            "transition": str,
        }
    ]
}


VOICE_PROMPT_SCHEMA = {
    "voice": {
        "language": str,
        "gender": str,
        "age": str,
        "accent": str,
        "pace": str,
        "style": str,
        "emotion": str,
        "energy": str,
        "pronunciation_notes": str,
        "pause_instructions": str,
        "voice_prompt": str,
    }
}


CHARACTER_PROFILE_SCHEMA = {
    "characters": [dict],
}