from odoo import fields, models


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Properties'

    name = fields.Char('Estate Property', required=True, translate=True)
    description = fields.Char()
    postcode = fields.Char()
    date_availability = fields.Date('Available from', default=lambda self: fields.Date.add(fields.Date.today(),months = 3), copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float('Selling price', readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Oriented',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        help="Oriented is used to show which cardinal direction the garden is oriented to")
    active=fields.Boolean("Active", default=False)
    state = fields.Selection(
        string='State',
        selection=[('new', 'New'), ('received', 'Offer Received'), ('accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')],
        required = True,
        default='new',
        copy=False,
        help="Shows the state of the property")

