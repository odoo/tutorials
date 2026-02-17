from odoo import models, fields

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "An offer for a specific property, made by a specific buyer at lower or higher price than the expected price"

    price = fields.Float(required=True)
    status = fields.Selection(
        string="Status",
        selection=[
            ('accepted', 'Accepted'), 
            ('refused', 'Refused')
        ], 
        copy=False,
    )
    partener_id = fields.Many2one("res.partner", string="Buyer", required=True)
    property_id = fields.Many2one("estate_property", string="Property", required=True)
