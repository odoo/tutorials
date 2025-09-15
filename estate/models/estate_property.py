from odoo import models, fields


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = "Estate Property"
    
    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(string="Available From")
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    type = fields.Many2one('estate.property.type', string="Property Type")
    tag_ids = fields.Many2many(
        'estate.property.tag', 
    )
    salesman_id = fields.Many2one(
        'res.users', 
        default=lambda self: self.env.user
    )
    
    buyer_id = fields.Many2one(
        'res.partner', 
        copy=False
    )
