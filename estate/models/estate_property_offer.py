from odoo import fields, models  # type: ignore


class EstatePropertyOffer(models.Model):
    _name = "estate_property_offer"
    _description = "estate property offer"

    price = fields.Float(string="Price")
    status = fields.Selection(
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
        copy=False,
        string="Status",
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate_property", required=True)
