from odoo import models, fields
class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Real Estate Property Type'
    _order = "sequence,name"
    sequence = fields.Integer(default=10)
    name = fields.Char(string="Type Name", required=True)
    property_type_id = fields.Many2one('estate.property.type', string="Property Type")
    buyer_id = fields.Many2one('res.partner', string="Buyer")
    seller_id = fields.Many2one('res.users', string="Salesperson", default=lambda self: self.env.user)
    property_ids = fields.One2many('estate.property', 'property_type_id', string="Properties")
    expected_price = fields.Float(string="Expected Price", required=True)
    state = fields.Selection(selection=[
        ('new', 'New'),
        ('received', 'Offer Received'),
        ('accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('cancelled', 'Cancelled'),
    ], default='new', string="Status", copy=False)  
    _sql_constraints = [
        ('unique_type_name', 'UNIQUE(name)',
         'The property type name must be unique.')
    ]


