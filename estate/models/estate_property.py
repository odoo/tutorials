from odoo import models, fields


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate properties"
    name = fields.Char('Property Name', required=True, translate=True)
    description = fields.Text('Property Description', required=True)
    postcode = fields.Char('Property postcode')
    date_availability = fields.Date('Property availability date', copy=False, default=fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float('Property expected price')
    selling_price = fields.Float('Property selling price', readonly=True)
    bedrooms = fields.Integer(default=2)
    active = fields.Boolean(default=True)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
    state = fields.Selection(
        string='State',
        required=True,
        default='new',
        copy=False,
        selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')])
