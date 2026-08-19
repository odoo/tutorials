from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate property"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
            'Availale From',
            copy=False,
            default=fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer('Living area (m²)')
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer('Garden area (m²)')
    garden_orientation = fields.Selection(
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        help="garden orientation in respect to main compass directions")
    active = fields.Boolean(default=True)
    state = fields.Selection(
            selection=[
                ('new', 'New'),
                ('offer_received', 'Offer Received'),
                ('offer_accepted', 'Offer Accepted'),
                ('sold', 'Sold'),
                ('cancelled', 'Cancelled')],
            default='new',
            help="State of the estate property")
        
