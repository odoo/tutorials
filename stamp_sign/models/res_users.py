from odoo import models, api


class ResUsers(models.Model):
    _inherit = "res.users"

    @api.model
    def get_current_user_company_details(self):
        user = self.env.user
        details = {
            "name": user.name,
            "company": user.company_id.name if user.company_id else "",
            "address": user.company_id.street if user.company_id else "",
            "city": user.company_id.city if user.company_id else "",
            "country": user.company_id.country_id.name
            if user.company_id and user.company_id.country_id
            else "",
            "vat": user.company_id.vat if user.company_id else "",
        }
        return details
