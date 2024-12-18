
from odoo import fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "An offer for a real estate property"

    price = fields.Integer()
    partner_id = fields.Many2one("res.partner", string="Partner", required=True, copy=False)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    status = fields.Selection(
            string="Status",
            selection=[('refused', 'Refused'), ('accepted', 'Accepted')]
    )
