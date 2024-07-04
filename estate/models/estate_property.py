from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Test Model"

    name = fields.Char(required=True)
    postcode = fields.Text()
    date_availability = fields.Date(default='3 months', copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default='2')
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(string='Type', selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
    active = fields.Boolean(default=True)
    state = fields.Selection(string='Type', selection=[('new', 'New'), ('offer received', 'Offer Received'), ('offer accepted', 'Offer Accepted'), ('sold', 'Sold'), ('canceled', 'Canceled')], copy=False, default='New')
