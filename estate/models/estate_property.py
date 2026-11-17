from odoo import fields, models

class RecurringPlan(models.Model):
    _name = "estate.property"
    _description = "Real estate"

    name = fields.Char(required=True, string='Title')
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Datetime(string='Available From',
                                        copy=False,
                                        default=fields.Date.add(fields.Date.today(), months=3))

    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()

    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Garden orientation',
        selection=[('north', 'North'), ('east', 'East'),
                   ('south', 'South'), ('west', 'West')],
        help="Type is used to separate Leads and Opportunities")

    # Reserved fields
    active = fields.Boolean(default=True)
    state = fields.Selection(
        default='new', required=True, copy=False,
        selection=[('new', 'New'), ('received', 'Offer Received'),
                   ('accepted', 'Offer Accepted'), ('sold', 'Sold'),
                   ('cancelled', 'Cancelled')])