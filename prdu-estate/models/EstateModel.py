from odoo import fields, models
from dateutil.relativedelta import relativedelta


class EstateModel(models.Model):
    _name = "test_estate_model"
    _description = "Unreal estate moves a lot more than real one"
    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date("Available From",copy=False, default=lambda self: fields.Datetime.now() + relativedelta(months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer("Living Area (m^2)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(selection=[("North", "North"), ("South", "South"), ("East", "East"), ("West", "West")])
    active = fields.Boolean(default=True)
    state = fields.Selection(selection=[("New", "New"), ("Offer Received", "Offer Received"), ("Offer Accepted", "Offer Accepted"), ("Sold", "Sold"), ("Cancelled", "Cancelled")],default='New')
