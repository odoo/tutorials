from odoo import fields, models
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Integer(string="Postcode")
    date_availability = fields.Date(
        string="Availability Date",
        default=lambda self:fields.Datetime.today() + relativedelta(days=90),
    )
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", default="20000",readonly=True, copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
    )
    active = fields.Boolean(string="Active")
    status = fields.Selection(
        string="Status",
        selection=[
            ("new", "New"),
            ("offer received", "Offer Received"),
            ("offer accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled")
        ],
    )

    # Relations

    # Relation for property type
    property_type_id = fields.Many2one(comodel_name = "estate.property.type", string="Property Type")

    # Relation for Partner
    partner_id = fields.Many2one("res.partner", string="Partner")
    user_id = fields.Many2one("res.users", string="User")



