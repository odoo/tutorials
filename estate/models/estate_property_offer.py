from odoo import fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offer for a property"

    price = fields.Float()
    status = fields.Selection([
        ('refused', 'Refused'),
        ('accepted', 'Accepted')
    ], copy=False)
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
