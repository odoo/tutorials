from odoo import fields, models


class EstatePropertyOffer(models.Model):
    _name = "realestate.properties.offer"
    _description = "Real estate property offer"

    price = fields.Float("Price")
    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("realestate.properties", required=True)
