from odoo import fields, models


class SignItemType(models.Model):
    _inherit = "sign.item.type"

    item_type = fields.Selection(
        selection_add=[
            ("stamp", "Stamp"),
        ],
        ondelete={"stamp": "set default"},
    )


class SignItem(models.Model):
    _inherit = "sign.item"

    stamp_company = fields.Char("Company")
    stamp_address = fields.Char("Address")
    stamp_city = fields.Char("City")
    stamp_country = fields.Char("Country")
    stamp_vat = fields.Char("VAT Number")
    stamp_logo = fields.Binary("Stamp Logo")

    def _get_stamp_details_for_user(self):
        self.ensure_one()
        user = self.env.user
        details = {}
        if user.has_group("base.group_user"):
            details = {
                "company": user.company_id.name,
                "address": user.company_id.street,
                "city": user.company_id.city,
                "country": user.company_id.country_id.name,
                "vat": user.company_id.vat,
            }
        return details
