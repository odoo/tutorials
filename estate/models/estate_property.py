# from odoo import models
# class EstateProperty(models.Model):
#     _name = "estate_property"
from odoo import models, fields
from datetime import timedelta


class EstateProperty(models.Model):
    # _name sẽ là tên bảng trong DB (chuyển thành library_book)
    _name = "estate.property"
    _description = "Bất động Sản"

    # Các cột (fields) trong bảng
    name = fields.Char(string="Title", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Integer(string="Postcode")
    date_availability = fields.Datetime(
        string="Available From",
        copy=False,
        default=lambda self: fields.Datetime.now() + timedelta(days=90),
    )
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly="1", copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Char(string="Living Area (sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage", default=True)
    garden = fields.Boolean(string="Garden", default=True)
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
        help="Type is used to separate North, South, East, West",
    )
    is_ative = fields.Boolean(string="Active", default=False)
    state = fields.Selection(
        string="State",
        selection=[
            ("new", "New"),
            ("offerReceived", "Offer Received"),
            ("offerAccepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
    )
