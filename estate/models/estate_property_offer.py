from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offers"

    price = fields.Float(required=True)
    status = fields.Selection(
        string="Status",
        selection=[('Accepted', 'Accepted'), ('Refused', 'Refused')],
        copy=False
    )
    partner_id = fields.Many2one("res.partner", string="Offer by")
    property_id = fields.Many2one("estate.property", string="Property")
