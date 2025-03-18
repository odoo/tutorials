from odoo import fields, models
from dateutil.relativedelta import relativedelta

class EstateProperty(models.Model):
    _name = "estate_property"
    _description = "My Estate Property"

    name = fields.Char(required = True)
    postcode = fields.Char()
    date_availability = fields.Date(copy = False, default = fields.Date.today() + relativedelta(months = 3))
    expected_price = fields.Float(required = True)
    selling_price = fields.Float(readonly = True, copy = False)
    bedrooms = fields.Integer(default = 2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
    active = fields.Boolean(default = True)
    state = fields.Selection([('new', 'New'), ('received', 'Offer Received'), ('accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')],
                             required = True, copy = False, default = 'new')
    description = fields.Char("Description.", default = "This is it.", readonly = True)

    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    salesman = fields.Many2one('res.users', string='Salesperson', index=True, default=lambda self: self.env.user)
    buyer = fields.Many2one('res.partner', string='Buyer', index=True, copy = False)

    tag_ids = fields.Many2many('estate.property.tag', string = 'Property Tags')
    offer = fields.One2many('estate.property.offer', 'property_id', string = 'Offers')

