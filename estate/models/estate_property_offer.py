from odoo import models, fields


class EstatePropertyOffer(models.Model):
    _name = "estate.property_offer"
    price = fields.Char(string="Price")
    status = fields.Selection(
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
        string="Status",
        copy=False,
    )
    partner_id = fields.Many2one(
        comodel_name="res.partner", string="Partner", required=True
    )
    property_id = fields.Many2one(
        comodel_name="estate_property", string="Property", required=True
    )
