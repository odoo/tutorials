import requests
from datetime import timedelta
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class PharmacyAIService(models.AbstractModel):
    _name = 'pharmacy.ai.service'
    _description = 'AI Service for Hugging Face'

    def _get_api_token(self):
        return self.env['ir.config_parameter'].sudo().get_param('HF_API_TOKEN')

    def _call_llm(self, messages, model="meta-llama/Llama-3.1-8B-Instruct:novita"):
        token = self._get_api_token()
        if not token:
            raise UserError(_("HF_API_TOKEN not set in system parameters."))

        API_URL = "https://router.huggingface.co/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        payload = {
            "messages": messages,
            "model": model,
            "temperature": 0.7,
            "max_tokens": 500
        }
        try:
            response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            result = response.json()
            return result['choices'][0]['message']['content']
        except requests.exceptions.RequestException as e:
            raise UserError(_("AI service error: %s") % str(e))

    def analyze_sentiment(self, text):
        messages = [
            {"role": "system",
             "content": "You are a customer sentiment analyst. Respond ONLY with one word: Positive, Neutral, or Negative."},
            {"role": "user", "content": f"Analyze the sentiment of this feedback: '{text}'"}
        ]
        return self._call_llm(messages)

    def chat(self, user_message, conversation_history=None):
        # Gather live data based on user message
        live_data = ""
        stock_info = self._get_medicine_stock_info(user_message)
        if stock_info:
            live_data += f"\n\nReal-time stock data:\n{stock_info}\n"
        orders_info = self._get_today_orders_info(user_message)
        if orders_info:
            live_data += f"\n{orders_info}\n"

        system_prompt = f"""
        You are a helpful assistant for the Pharma Control Center Odoo module. Features include medicine catalog, patient management, cart ordering, dashboard, role-based access, drug interaction warnings, reports, etc.
        {live_data}
        Answer the user's question accurately using the live data if relevant. Always remind users to consult a doctor for medical advice. Keep answers concise and friendly.
        """
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
        return self._call_llm(messages), []

    def _get_medicine_stock_info(self, user_message):
        """Extract medicine name from message and return stock info."""
        medicines = self.env['pharmacy.medicine'].search_read([], ['name', 'quantity'])
        for med in medicines:
            if med['name'].lower() in user_message.lower():
                return f"Medicine '{med['name']}' has {med['quantity']} units in stock."
        # Also try to match partial names
        for med in medicines:
            if any(word in med['name'].lower() for word in user_message.lower().split()):
                return f"Medicine '{med['name']}' has {med['quantity']} units in stock."
        return None

    def _get_today_orders_info(self, user_message):
        keywords = ['today order', 'orders today', "today's orders", 'todays orders']
        if any(kw in user_message.lower() for kw in keywords):
            today = fields.Date.today()
            orders = self.env['sale.order'].search([
                ('date_order', '>=', today),
                ('date_order', '<', today + timedelta(days=1)),
                ('state', 'not in', ['cancel'])
            ])
            if orders:
                total = sum(orders.mapped('amount_total'))
                return f"Today there are {len(orders)} orders, total amount: {total}."
            else:
                return "No orders placed today."
        return None