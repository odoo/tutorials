from odoo import models, fields

class EstateProperty(models.Model):
    _name = "estate.property.offer"
    _description = "Estate property offers"


    price = fields.Float(required=True)
    status = fields.Selection(
        selection=[
            ('refused', 'Refused'), 
            ('accepted', 'Accepted')
        ], 
        copy=False
    )

    # relations
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
