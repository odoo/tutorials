from odoo import fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate_offer"
    _description = "This is to say that this is the desctiption of the estate offer"

    price = fields.Float("Price")
    status = fields.Selection(
        string="Status",
        copy=False,
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
    )
    partner_id = fields.Many2one(
        "res.partner",
        required=True,
    )
    property_id = fields.Many2one("estate_model", required=True)
