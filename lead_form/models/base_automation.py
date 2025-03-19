from odoo import models


class CustomWebhookAutomation(models.Model):
    _inherit = 'base.automation'

    def _execute_webhook(self, payload):
        """Override the method to create a lead from an ads via webhook."""

        lead = self.env['crm.lead'].create_lead_from_ads(payload)
        if lead:
            return lead

        return super()._execute_webhook(payload)
