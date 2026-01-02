from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property Planning"

    name = fields.Char("Name", required=True, default="Unknown")
    description = fields.Text("Description")
    postcode = fields.Char("Postcode")
    date_availability = fields.Date(
        "Available From", copy=False, default=fields.Datetime.now
    )
    expected_price = fields.Float("Expected Pice", required=True)
    selling_price = fields.Float("Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer("Bedrooms", default=2)
    living_area = fields.Integer("Living Area")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden Area")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[("n", "North"), ("w", "West"), ("e", "East"), ("s", "South")],
    )
    active = fields.Boolean("Active", default=True)
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer received", "Offer Received"),
            ("offer Accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        default="new",
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    seller = fields.Many2one(
        "res.users", string="Salesman", default=lambda self: self.env.user
    )
    buyer = fields.Many2one("res.partner", string="Buyer", copy=False)
    tags = fields.Many2many("estate.property.tag")
    offer = fields.One2many("estate.property.offer", "property_id")
