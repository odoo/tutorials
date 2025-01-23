from odoo import models, fields

class EstatePropertyOffer(models.Model):

    _name = "estate.property.offer"
    _description = "The offers for a property"

    price = fields.Float(name = "Price", required = True)
    status = fields.Selection(string='Status',
        selection=[('accepted', 'Accepted'), 
                   ('refused', 'Refused'), 
                   ],
        help="What was the answer to the offer ?")
    partner_id = fields.Many2one("res.partner", required=True, name="Partner")
    property_id = fields.Many2one("estate.property", required=True)
