from odoo import fields, models


class EstateOffer(models.Model):
    _name = "estate.offer"
    _description = "An estate offer"

    price = fields.Float()
    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")], copy=False
    )

    # Foreign fields
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
