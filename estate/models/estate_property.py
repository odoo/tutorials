from odoo import fields, models


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Handle real estate property'

    name = fields.Char(required=True, string="Title")
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, string="Available From", default=fields.Date.today)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        string='Garden orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string='Status',
        selection=[('new', 'New'), ('offer_received', 'Offer Received'),
                   ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')],
        required=True,
        copy=False,
        default='new',
    )
