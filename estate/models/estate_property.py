from odoo import models, fields

class EstateProterty(models.Model):
    _name = "estate_property"
    _description = "estate property"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(default= fields.Date.today(), copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(copy=False, readonly=True)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientaton = fields.Selection(
        selection=[('north','North'), ('south','South'),
                     ('east', 'East'), ('west','West')]
    )

    active = fields.Boolean(default=True, active=False)
    state = fields.Selection(
        default='new',
        copy=False,
        required=True,
        selection=[('new', 'New'), ('offer received', 'Offer Received'),
                   ('offer accepted', 'Offer Accepted'), ('sold', 'Sold'),
                   ('canceled', 'Canceled')]
    )
