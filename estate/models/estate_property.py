from odoo import fields,models
from datetime import timedelta

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'real estate property'

    name= fields.Char(required=True) 
    description=fields.Text()
    postcode=fields.Char()
    date_availability=fields.Date(copy= False,default=lambda self: fields.Date.today() + timedelta(days=90))
    expected_price=fields.Float(required=True)
    selling_price=fields.Float(readonly=True, copy= False)
    bedrooms=fields.Integer(default=2)
    living_area=fields.Integer()
    facades=fields.Integer()
    garage=fields.Boolean()
    garden=fields.Boolean()
    garden_area=fields.Integer()
    garden_orientation=fields.Selection(
        selection=[
            ('north','North'),
            ('south','South'),
            ('east','East'),
            ('west','West')
        ],
        default='north', required=True
    )
    active=fields.Boolean(default=True)
    state=fields.Selection(
        selection=[
            ('new','New'),
            ('offer_received','Offer Received'),
            ('offer_accepted','Offer Accepted'),
            ('sold','Sold'),
            ('cancel','Cancel')
        ],
        default='new', required=True
    )
    property_type_id=fields.Many2one('estate.property.type', string='real estate property type')
    partner_id = fields.Many2one('res.partner', string='Partner', copy= False)
    user_id = fields.Many2one('res.users', string="Users", default=lambda self: self.env.user)
    tag_ids = fields.Many2many('estate.property.tag', string='Tag')
    offer_ids = fields.One2many('estate.property.offer', 'property_id',string='Offer')
