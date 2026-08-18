from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property Model"

    name = fields.Char("Property Name", required=True)
    description = fields.Text("Description")
    postcode = fields.Char("Postcode")
    date_availability = fields.Date(
        "Availability Date",
        default=lambda self: fields.Date.add(fields.Date.today(), months=3),
        copy=False,
    )
    expected_price = fields.Float("Expected Price", required=True)
    selling_price = fields.Float("Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer("Bedrooms", default=2)
    living_area = fields.Integer("Living Area")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden Area")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"),
            ("east", "East"),
            ("south", "South"),
            ("west", "West"),
        ],
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancel", "Cancelled"),
        ],
        default="new",
    )
    active = fields.Boolean("Active", default=True)

    # Many2one references
    type_id = fields.Many2one(comodel_name="estate.property.type")
    buyer_id = fields.Many2one(string="Buyer", comodel_name="res.partner")
    salesperson_id = fields.Many2one(
        string="Salesperson",
        comodel_name="res.users",
        default=lambda self: self.env.user,
    )

    # One2many references
    offer_ids = fields.One2many(
        comodel_name="estate.property.offer",
        inverse_name="property_id",
    )

    # Many2many references
    tag_ids = fields.Many2many(
        string="Tags",
        comodel_name="estate.property.tag",
    )
