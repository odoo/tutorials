from odoo import fields, models

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'

    name = fields.Char('Property Name', required=True)
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Available from', default=lambda self: fields.Date.add(fields.Date.context_today(self), months=3), copy=False)
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling price', readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Living Area')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area')
    garden_orientation = fields.Selection(string='Garden Orientation', selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
    active = fields.Boolean('Active', default=True)
    status = fields.Selection(string='Status', selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', "cancelled")], default='new')
    # Many to one relation with property type model
    property_type_id = fields.Many2one('estate.property.type', string='Property type')
    # Customer
    partner_id = fields.Many2one('res.partner', string='Buyer', index=True)
    # Internal User
    user_id = fields.Many2one('res.users', string='Salesman', index=True, tracking=True, default=lambda self: self.env.user)
    # Many to many relation with Tags model
    tag_ids = fields.Many2many('estate.property.tag', string='Property Tag')
    # One to many relation with offer model
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')
