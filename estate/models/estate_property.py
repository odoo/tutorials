from odoo import fields, models


class Estate(models.Model):
    _name = "estate.property"
    _description = "Properties of estate entities."

    name = fields.Char(string="Name", required=True)
    description = fields.Text()
    active = fields.Boolean(default=True)
    postcode = fields.Char()
    date_availability = fields.Date(
            copy=False,
            default=fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float(required=True, readonly=True)
    selling_price = fields.Float(copy=False, readonly=True)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
            string='Orientation',
            selection=[
                ('North', 'north'),
                ('South', 'south'),
                ('East', 'east'),
                ('West', 'east')],
            help="Cardinal orientation of the garden.",
        )
    state = fields.Selection(
            string='State',
            required=True,
            copy=False,
            default='New',
            selection=[('New', 'new'),
                       ('Offer Received', 'offer received'),
                       ('Offer Accepted', 'Offer Accepted'),
                       ('Sold', 'sold'),
                       ('Canceled', 'Canceled')])
