from dateutil.relativedelta import relativedelta

from odoo import fields, models


def _default_date_availability(args):
    return fields.Date.today() + relativedelta(months=3)


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = "Estate Property"
    name = fields.Char(required=True, string='Title')
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False,
                                    default=_default_date_availability,
                                    string='Available from')
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string='Living area (sqm)')
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string='Garden area (sqm)')
    garden_orientation = fields.Selection(
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
    active: bool = fields.Boolean(default=True)
    state = fields.Selection(copy=False, default='New', required=True,
                             selection=[('New', 'New'), ('Offer Received', 'Offer Received'),
                                        ('Offer Accepted', 'Offer Accepted'), ('Sold', 'Sold'),
                                        ('Cancelled', 'Cancelled')])
