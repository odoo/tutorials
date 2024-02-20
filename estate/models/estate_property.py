from odoo import models, fields


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    name = fields.Char(string='Title', required=True)
    description = fields.Text(string='Property Description')
    postcode = fields.Char(string='Postcode')
    date_availability = fields.Date(string='Available From', copy=False,
                                    default=fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float(string='Expected Price', required=True)
    selling_price = fields.Float(string='Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer(string='Bedrooms', default=2)
    living_area = fields.Integer(string='Living Area (sqm)')
    facades = fields.Integer(string='Facades')
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    garden_area = fields.Integer(string='Garden Area')
    garden_orientation = fields.Selection(string='Garden Orientation', selection=[('north', 'North'),
                                                                                  ('south', 'South'),
                                                                                  ('east', 'East'),
                                                                                  ('west', 'West')])
    active = fields.Boolean(string='Active', default=True)
    state = fields.Selection(string='State', selection=[('new', 'New'),
                                                        ('offer_received', 'Offer Received'),
                                                        ('offer_accepted', 'Offer Accepted'),
                                                        ('sold', 'Sold'),
                                                        ('cancelled', 'Canceled')],
                             required=True, default='new', copy=False)
