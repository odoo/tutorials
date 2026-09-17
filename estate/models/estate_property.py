from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate_property"
    _description = "This is the model for the real estate property :)"
    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=fields.Datetime.add(fields.Datetime.today(), months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(string='Orientation',
    selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')], help="Garden Orientation (North, South, East, West)")
    active = fields.Boolean(default=True)
    stage = fields.Selection(string="Stage",
    selection=[("new", "New"), ("offer received", "Offer Received"), ("offer accepted", "Offer Accepted"), ("sold", "Sold"), ("cancelled", "Cancelled")],
    required=True, default="new", copy=False)
