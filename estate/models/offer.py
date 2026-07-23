from odoo import fields, models


class Offer(models.Model):
    _name = "estate_property_offer"
    _description = "Offer made to some estate (property)"

    price = fields.Float(string="Price")
    status = fields.Selection(
        string="Status",
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
        copy=False,
    )
    property_id = fields.Many2one(
        string="Property", comodel_name="estate_property", required=True
    )
    partner_id = fields.Many2one(
        string="Partner", comodel_name="res.partner", required=True
    )
