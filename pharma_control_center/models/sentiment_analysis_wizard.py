from odoo import models, fields, api, _

class SentimentAnalysisWizard(models.TransientModel):
    _name = 'sentiment.analysis.wizard'
    _description = 'Sentiment Analysis Wizard'

    feedback_text = fields.Text(string="Customer Feedback", required=True)
    sentiment_result = fields.Text(string="Sentiment", readonly=True)

    def action_analyze(self):
        ai_service = self.env['pharmacy.ai.service']
        self.sentiment_result = ai_service.analyze_sentiment(self.feedback_text)
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'sentiment.analysis.wizard',
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }