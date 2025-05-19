from odoo import fields, models
from dateutil.relativedelta import relativedelta

class Estate_property(models.Model):
    _name = "estate.property"
    _description = "Model to modelize Real Estate objects"

    name = fields.Char(string="Name", required=True)
    description  = fields.Text()
    postcode = fields.Char()
    date_availabilty = fields.Datetime(copy=False, default=fields.date.today() + relativedelta(months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Orientation',
        selection=[('north','North'), ('south','South'),('east','East'),('west','West')],
        help="Orientation is meant to describe the garden"
    )
    active = fields.Boolean('Active', default=True)
    state = fields.Selection(
        string='Status',
        selection=[('new','New'), ('offer_received','Offer Received'),('offer_accepted','Offer Accepted'),('sold','Sold'),('cancelled', 'Cancelled')],
        help="Orientation is meant to describe the garden",
        default='new',
        copy=False
    )
