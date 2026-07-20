from odoo import fields, models


class Property(models.Model):
    _name = "estate.property"
    _description = "Properties of our managed estates"

    name = fields.Char(string='Name', default="Unknown", required=True)
    active = fields.Boolean(default=True)
    state = fields.Selection(required=True, default='new', copy=False, selection=[
        ('new', 'New')
        , ('offer_received', 'Offer Received')
        , ('offer_accepted', 'Offer Accepted')
        , ('sold', 'Sold')
        , ('cancelled', 'Cancelled'),
    ])

    description = fields.Text(string='description')
    postcode = fields.Char(string='postcode')
    date_availability = fields.Date(string='Available from', default=lambda _: fields.Date.add(fields.Date.today(), months=3), copy=False)
    expected_price = fields.Float(string='expected price', required=True)
    selling_price = fields.Float(string='selling price', readonly=True, copy=False)
    bedrooms = fields.Integer(string='# bedrooms', default=2)
    living_area = fields.Integer(string='living area size')
    facades = fields.Integer(string='# facades')
    garage = fields.Boolean(string='Has garage')
    garden = fields.Boolean(string='Has garden')
    garden_area = fields.Integer(string='garden area size')
    garden_orientation = fields.Selection(string='garden orientation',
    selection=[
        ('north', 'North')
        , ('south', 'South')
        , ('east', 'East')
        , ('west', 'West')])
