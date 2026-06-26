import requests
from odoo.exceptions import UserError
from odoo import _

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent"


def _get_api_key(env):
    api_key = env['ir.config_parameter'].sudo().get_param('ai.google_key')
    if not api_key:
        raise UserError(_("Please configure the Google API key in Settings."))
    return api_key


def ask_ai(env, prompt):
    headers = {
        "x-goog-api-key": _get_api_key(env),
        "Content-Type": "application/json"
    }
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseMimeType":"application/json",
            "responseSchema":{
                "type":"object",
                "properties":{
                    "answer":{"type":"string"},
                    "message_ids":{
                        "type":"array",
                        "items":{"type":"integer"}
                    }
                },
                "required":["answer","message_ids"]
            }
        }
    }
    response = requests.post(GEMINI_URL, headers=headers, json=payload, timeout=60)
    response.raise_for_status()
    data = response.json()
    return  data['candidates'][0]['content']['parts'][0]['text']
  
def ask_ai_summarize(env, prompt):
    headers = {
        "x-goog-api-key": _get_api_key(env),
        "Content-Type": "application/json"
    }
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    response = requests.post(GEMINI_URL, headers=headers, json=payload, timeout=60)
    response.raise_for_status()
    data = response.json()
    return  data['candidates'][0]['content']['parts'][0]['text']