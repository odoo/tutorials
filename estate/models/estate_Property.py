from datetime import timedelta
from odoo import api, fields, models


class EstateModel(models.Model):
    _name = "estate.property"
    _description = "Estate model help save data"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        "Availability From",
        default=lambda self: fields.Date.today() + timedelta(days=90),
        copy=False,
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float("Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer("Number of Bedrooms", default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        [("north", "North"), ("east", "East"), ("south", "South"), ("west", "West")],
        string="Garden Orientation",
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    active = fields.Boolean("Active", default=True)
    state = fields.Selection(
        string="State",
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        default="new",
        copy=False,
        required=True,
    )

    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson_id = fields.Many2one(
        "res.users",
        string="SalesPerson",
        index=True,  # for index in database
        tracking=True,  # changes to this field -> to be logged in chatter
        default=lambda self: self.env.user,
    )

    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many(
        "estate.property.offer", "property_id"
    )  # all fields of offer will be shown in form view

    total_area = fields.Float(compute="_compute_total_area", string="Total Area(sqm)")
    best_price = fields.Float(compute="_compute_best_price", string="Best Price")

    @api.depends("living_area", "garden_area", "garden")
    def _compute_total_area(self):
        for record in self:
            if record.garden:
                record.total_area = (record.living_area or 0) + (
                    record.garden_area or 0
                )
            else:
                record.total_area = record.living_area or 0

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"), default=0.0)
