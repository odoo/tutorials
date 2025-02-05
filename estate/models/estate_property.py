from odoo import fields, models
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "This is estate model"

    name = fields.Char(string = "Name", required = True)
    description = fields.Text(string = "Description", required = True)
    postcode = fields.Char(string = "Postcode")
    date_availability = fields.Date(string = "Date Availability", copy=False, default = fields.Datetime.today()+relativedelta(days=90))
    expected_price = fields.Float(string = "Expected Price")
    selling_price = fields.Float(string = "Selling Price", copy=False, readonly=True)
    bedrooms = fields.Integer(string = "Bedrooms", default=2)
    living_area = fields.Integer(string = "Living Area")
    facades = fields.Integer(string = "Facades")
    garage = fields.Boolean(string = "Garage")
    garden = fields.Boolean(string = "Garden")
    garden_area = fields.Integer(string = "Garden Area")
    last_seen = fields.Datetime(string = "Last Seen", default=fields.Datetime.now())
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"), 
            ("south", "South"), 
            ("east", "East"),
            ("west", "West"),
        ],
    )
    active = fields.Boolean(string = "Active", default=True)
    state = fields.Selection(
        string="Status",
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled"),
        ],
        required=True,
        copy=False,
        default="new",
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
