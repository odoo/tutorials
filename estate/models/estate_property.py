from odoo import fields, models


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property'

    name = fields.Char('Property Name', required=True)
    active = fields.Boolean(default=False)
    postcode = fields.Char()
    date_availability = fields.Datetime(copy=False, default=fields.Datetime.add(fields.Datetime.today(), months=3))
    expected_price = fields.Float()
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[('north', 'North'), ('east', 'East'), ('south', 'South'), ('west', 'West')],
        help="Type is used to separate Leads and Opportunities")
    state = fields.Selection(
        selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')],
        required=True,
        default='new',
        copy=False,
    )
