from odoo import fields, models
import datetime

class TestModel(models.Model):
    _name = "estate_property_model"
    _description = "Estate property model test description"

    name = fields.Char(default="Unknown", required=True)
    description = fields.Text("Description of the Estate Propert Model")
    postcode = fields.Char("Post code")
    date_availability = fields.Date("Availability date", default=datetime.date.today() + datetime.timedelta(days=90), copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(copy=False, readonly=True)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([("north", "North"), ("south", "South"), ("west", "West"), ("east", "East")])
    active = fields.Boolean(default=True)
    state = fields.Selection([("new", "New"), ("offer_received", "Offer Received"), ("offer_accepted", "Offer Accepted"), ("sold", "Sold"), ("cancelled", "Cancelled")], default="new")