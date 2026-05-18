import json
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class PharmacyChatbot(models.TransientModel):
    _name = 'pharmacy.chatbot'
    _description = 'AI Pharmacy Assistant'

    chat_history = fields.Text(string="Chat History", readonly=True, default="")
    user_message = fields.Text(string="Your Message")  # not required

    def action_send_message(self):
        if not self.user_message:
            raise UserError(("Please enter a message."))

        user_entry = f"🧑‍⚕️ You: {self.user_message}\n"
        new_history = (self.chat_history + user_entry) if self.chat_history else user_entry

        ai_service = self.env['pharmacy.ai.service']
        try:
            response, _ = ai_service.chat(self.user_message, [])
            ai_entry = f"🤖 Assistant: {response}\n\n"
            new_history += ai_entry
        except UserError as e:
            ai_entry = f"🤖 Assistant: Error - {str(e)}\n\n"
            new_history += ai_entry

        self.chat_history = new_history
        self.user_message = False

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'pharmacy.chatbot',
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }