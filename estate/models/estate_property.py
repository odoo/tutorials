from odoo import fields, models

from datetime import datetime, timedelta


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"

    # Basic property details
    name = fields.Char(
        string="Name",
        help="The name of the property.",
        required=True
    )
    description = fields.Text(
        string="Description",
        help="Detailed description of the property."
    )
    postcode = fields.Char(
        string="Postcode",
        help="Postal code where the property is located."
    )
    # Availability and pricing
    date_availability = fields.Date(
        string="Available From",
        help="The date when the property becomes available.",
        copy=False,
        default= datetime.now() + timedelta(days=90)
    )
    expected_price = fields.Float(
        string="Expected Price",
        help="The expected selling price of the property.",
        required=True,
    )
    selling_price = fields.Float(
        string="Selling Price",
        help="The final selling price of the property. It cannot be manually edited.",
        readonly=True,
        copy=False
    )
    # Property characteristics
    bedrooms = fields.Integer(
        string="Bedrooms",
        help="Number of bedrooms in the property.",
        default=2
    )
    living_area = fields.Integer(
        string="Living Area (sqm)",
        help="Total living area in square meters."
    )
    facades = fields.Integer(
        string="Facades",
        help="Number of facades the property has."
    )
    garage = fields.Boolean(
        string="Garage",
        help="Indicates if the property has a garage."
    )
    garden = fields.Boolean(
        string="Garden",
        help="Indicates if the property has a garden."
    )
    garden_area = fields.Integer(
        string="Garden Area (sqm)",
        help="Total garden area in square meters."
    )
    # Garden orientation with selection options
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        help="The direction the garden faces.",
        selection=[
            ("east", "East"),
            ("west", "West"),
            ("north", "North"),
            ("south", "South")
        ]
    )
    active = fields.Boolean(
        string="Active",
        help="If unchecked, it will allow you to hide the property without removing it.",
        default=True
    )
    state = fields.Selection(
        string="State",
        help="State of the property",
        selection=[('new', 'New'),
                   ("offer_received", "Offer Received"),
                   ("offer_accepted", "Offer Accepted"),
                   ("sold", "Sold"), ("canceled", "Canceled")],
        default='new',
        copy=False
    )
    property_type_id = fields.Many2one(
        string="Property Type",
        help="Type of property.",
        comodel_name="estate.property.type"
    )
    buyer_id = fields.Many2one(
        string="Buyer",
        help="The buyer of the property.",
        copy=False,
        comodel_name="res.partner"
    )
    salesperson_id = fields.Many2one(
        string="Salesperson",
        help="The salesperson responsible for the property.",
        default=lambda self: self.env.user,
        comodel_name="res.users"
    )
