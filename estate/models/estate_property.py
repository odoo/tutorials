from odoo import fields, models
from dateutil.relativedelta import relativedelta

class TestModel(models.Model):
    _name = "estate.property"
    _description = "test estate model"

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)
    state = fields.Selection(
        required=True,
        copy=False,
        default="new",
        selection=[("new", "New"), ("offer received", "Offer Received"), ("offer accepted", "Offer Accepted"), ("sold", "Sold"), ("cancelled","Cancelled")]
    )
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Datetime(copy=False, default=fields.Datetime.today() + (relativedelta(months=3)))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='type',
        selection=[('north', 'North'), ('south', 'South'), ('East', 'east'), ('West', 'west')]
    )
