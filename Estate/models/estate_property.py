from odoo import fields, models
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    name = fields.Char(default="New Estate")
    description = fields.Char()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=fields.Datetime.now() + relativedelta(months=3))
    expected_price = fields.Float()
    selling_price = fields.Float(readonly=True, copy=False)
    bedroom = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    active = fields.Boolean(default=True)
    garden_orientation = fields.Selection(
        string='garden',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')]
    )
    state = fields.Selection(
        string='state',
        selection=[('new', 'New'), ('offer_accepted', 'Offer accepted'), ('sold', 'Sold'), ('offer_recieved', 'Offer recieved'), ('canceled', 'Canceled')], copy=False, default='new'
    )
