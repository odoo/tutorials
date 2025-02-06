# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Contains all properties related to estate model"

    # Basic Details
    name = fields.Char(string="Title", required=True)
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(
        string="Available From", copy=False, default=lambda self: fields.Date.add(fields.Date.today(), months=3)
    )
    tag_ids = fields.Many2many(
        string="Property Tags", comodel_name="estate.property.tag"
    )
    property_type_id = fields.Many2one(
        string="Property Type", comodel_name="estate.property.type"
    )
    offer_ids = fields.One2many(
        string="Offers", comodel_name="estate.property.offer", inverse_name="property_id", copy=False
    )
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(
        string="Selling Price", readonly=True, copy=False
    )

    # Description Fields
    description = fields.Text(string="Description")
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    facades = fields.Integer(string="Facades")
    living_area = fields.Integer(string="Living Area (sqm)")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West")
        ]
    )
    total_area = fields.Integer(
        string="Total Area (sqm)", compute="_compute_total_area"
    )
    best_price = fields.Float(
        string="Best Price", compute="_compute_best_price")

    # Other Info
    buyer_id = fields.Many2one(string="Buyer", comodel_name="res.partner")
    salesperson_id = fields.Many2one(
        string="Salesperson",
        comodel_name="res.users",
        default=lambda self: self.env.user
    )

    # Reserved Fields Override
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled")
        ],
        required=True,
        default="new"
    )
    active = fields.Boolean(default=True)

    @api.depends('garden_area', 'living_area')
    def _compute_total_area(self):
        self.total_area = self.garden_area + self.living_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        self.best_price = max([x.price for x in self.offer_ids], default=0)

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = None
