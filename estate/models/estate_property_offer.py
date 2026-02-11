from odoo import fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "estate property offer model"

    price = fields.Char("Price")
    status = fields.Selection(
        string="Status",
        selection=[("accepted", "Accepted"), ("rejected", "Rejected")],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
