from odoo import fields, models


class Property(models.Model):
    _name = "estate.property"
    _description = "Estate properties"

    name = fields.Char("Title", required=True)
    description = fields.Text("Description")
    postcode = fields.Char("Postcode")
    date_availability = fields.Date("Available From", copy=False, default=fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float("Expected Price", required=True)
    selling_price = fields.Float("Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer("Bedrooms", default=2)
    living_area = fields.Integer("Living Area (sqm)")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden Area (sqm)")
    garden_orientation = fields.Selection(
        [("north", "North"),
        ("south", "South"),
        ("east", "East"),
        ("west", "West")],
        "Garden Orientation")
    status = fields.Selection(
        [("new", "New"),
         ("offer_received", "Offer Received"),
         ("offer_accepted", "Offer Accepted"),
         ("sold", "Sold"),
         ("cancelled", "Cancelled")],
        default="new", string="Status", required=True, copy=False)
    active = fields.Boolean(default=True)
