from odoo import  fields,models
from datetime import date
from dateutil.relativedelta import relativedelta

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property is defined"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_avaiblity = fields.Date(copy = False, default = date.today()+ relativedelta(months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly = True, copy = False)
    bedrooms = fields.Integer(default = 2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string = 'Direction',
        selection=[('north','North'), ('south','South'), ('east','East'), ('west','West')],
        help = "This is used to locate garden's direction"
    )
    active = fields.Boolean(default = True)
    state = fields.Selection(
        selection=[('new','New'), ('offer received','Offer Received'), ('offer acceptedt','Offer Accepted'), ('sold','Sold'), ('cancelled', 'Cancelled')],
        default = 'new',
        required = True,
        copy = False,
    )