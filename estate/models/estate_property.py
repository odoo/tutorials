from odoo import models, fields
from dateutil.relativedelta import relativedelta
from datetime import date
class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property Data"
    name = fields.Char(required=True)
    description = fields.Char()
    postcode = fields.Char()
    date_availability = fields.Date(default=date.today() + relativedelta(months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float()
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    active = fields.Boolean(default=True)
    state = fields.Selection(default='new', 
                             selection=[('new', 'New'), 
                             ('offer_recived', 'Offer Recieved'), 
                             ('offer_accepted', 'Offer Accepted'), 
                             ('sold', 'Sold'), ('canceled', 'Canceled')])
    garden_orientation = fields.Selection(selection=[('north', 'North'), 
                                                     ('south', 'South'), 
                                                     ('east', 'East'), 
                                                     ('west', 'West')])
    property_type_id = fields.Many2one("estate.property.type", string='Property Type')
    salesman_id = fields.Many2one(
        'res.users',          # The model this field relates to
        string='Salesman',      # Label for the field
        default=lambda self: self.env.user.partner_id # Set default to the current user's partner
    )
    buyer_id = fields.Many2one(
        'res.partner',          # The model this field relates to
        string='Buyer',         # Label for the field
        copy=False              # Prevent the field value from being copied when duplicating the record
    )

    tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    offer_ids = fields.One2many('estate.property.offer', 'property_id')
