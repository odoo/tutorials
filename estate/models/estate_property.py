from odoo import fields, models


class Property(models.Model):
    _name = "estate.property"
    _description = "Estate Propety Model"

    name = fields.Char(
        "Property Name", required=True,
        help="This field specifies the estate property name.",
    )
    description = fields.Text(
        "Property Description",
        help="This field specifies the description of property in brief to provide insights on the property.",
    )
    postcode = fields.Char(
        "Post Code", help="This field specifies the postcode of the property address."
    )
    date_availability = fields.Date(
        "Date Of Availability",
        help="This field specifies the date when the property will be available.",
    )
    expected_price = fields.Float(
        "Expected Price", required=True,
        help="This field specifies the price expected for the property.",
    )
    selling_price = fields.Float(
        "Selling Price",
        help="This field specifies the actual selling price of the property.",
    )
    bedrooms = fields.Integer(
        "Number Of Bedrooms",
        help="This field specifies the number of bedroom that this property consists of.",
    )
    living_area = fields.Integer(
        "Living Area (sqm)",
        help="This field specifies the size of living area (in sqm.) of the property.",
    )
    facades = fields.Integer(
        "Facades",
        help="This field specifies the facade i.e. the exterior or the front of a property.",
    )
    garage = fields.Boolean(
        "Garage",
        help="This field specifies if the property has a garage",
    )
    garden = fields.Boolean(
        "Garden",
        help="This field specifies if the property has a garden",
    )
    garden_area = fields.Integer(
        "Garden Area (sqm)",
        help="This field specifies the size of garden area (in sqm.) of the property.",
    )
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
        help="This selection fields specifies the facing direction of garden (North, South, East, or West).",
    )
