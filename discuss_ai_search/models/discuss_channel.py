from odoo import models
from odoo.tools import html2plaintext
import json
from odoo.addons.mail.tools.discuss import Store
from . import discuss_ai


class DiscussChannel(models.Model):
    _inherit = "discuss.channel"
    
    def action_ask_ai(self, user_prompt):
        self.ensure_one()

        messages = self.message_ids.filtered(lambda m: m.message_type == 'comment').sorted('id')
        if not messages:
            return "There are no messages in this conversation yet.", {}, []

        lines = messages.mapped(
            lambda m: f"[{m.id}] {m.author_id.name}: {html2plaintext(m.body)}"
        )

        conversation = "\n".join(lines)

        prompt = f"""You are answering a question about a team chat conversation.
Use ONLY the messages below. Each line starts with its message id in brackets, e.g. "[42]".
Answer in 2-4 plain sentences, written naturally for a human to read.
The "answer" field must contain ONLY natural language prose. Do NOT include any
message ids, numbers in brackets like "[42]", or a trailing list of numbers
(e.g. "...,22,23,24,25") anywhere in the answer text.
Put the ids of the messages you relied on ONLY in the separate message_ids field (at most 5).

Conversation:
{conversation}

User Prompt: {user_prompt}
"""
        text = discuss_ai.ask_ai(self.env, prompt)
        result = json.loads(text)
        breakpoint()
        answer = result['answer']
        message_ids = result['message_ids']
        references = self.env['mail.message'].browse(message_ids).exists()
        store_data = Store().add(references).get_result()
        return answer, store_data, references.ids


    def action_summarize_ai(self):
        self.ensure_one()

        messages = self.message_ids.filtered(lambda m: m.message_type == 'comment').sorted('id')
        if not messages:
            return "There are no messages in this conversation yet."

        lines = messages.mapped(
            lambda m: f"{m.author_id.name}: {html2plaintext(m.body)}"
        )
        conversation = "\n".join(lines)

        prompt = f"""Summarize the conversation below in a short paragraph, then add a heading
"Key points:" in bold, followed by the key decisions made as a bullet list.
Format the entire response as simple HTML using only <p>, <strong>, <ul>, and <li> tags.
Do NOT use markdown syntax (no "*", "#", "**") and do NOT wrap the output in
a code block.

Conversation:
{conversation}
"""
        summary = discuss_ai.ask_ai_summarize(self.env, prompt)
        return summary
