from odoo import models, api, fields
import base64


class ResUsers(models.Model):
    _inherit = "res.users"

    stamp_sign = fields.Binary(string="Digital Stamp", copy=False, groups="base.group_user")
    stamp_sign_frame = fields.Binary(string="Digital Stamp Frame", copy=False, groups="base.group_user")

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
            "logo_url": False,
        }
        if user.company_id and user.company_id.logo:
            details["logo_url"] = "data:image/png;base64," + base64.b64encode(
                user.company_id.logo
            ).decode("utf-8")
        return details
