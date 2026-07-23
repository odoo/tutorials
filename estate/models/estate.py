from dateutil.relativedelta import relativedelta

from odoo import fields, models


class Estate(models.Model):
    _name = "estate_property"
    _description = "Real Estate"

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(
        string="Available From",
        default=fields.Date.today() + relativedelta(months=3),
        copy=False,
    )
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling price", readonly=True, copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"),
            ("east", "East"),
            ("west", "West"),
            ("south", "South"),
        ],
    )
    active = fields.Boolean(string="Active", default=True)
    state = fields.Selection(
        string="State",
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
    type_id = fields.Many2one(
        string="Property Type",
        comodel_name="estate_property_type",
    )
    salesman_id = fields.Many2one(
        string="Salesman",
        comodel_name="res.users",
        default=lambda self: self.env.user,
    )
    buyer_id = fields.Many2one(string="Buyer", comodel_name="res.partner", copy=False)
    tag_ids = fields.Many2many(string="Tags", comodel_name="estate_property_tag")
    offer_ids = fields.One2many(
        string="Offers",
        comodel_name="estate_property_offer",
        inverse_name="property_id",
    )
