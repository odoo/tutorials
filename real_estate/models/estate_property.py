from datetime import date, timedelta
from odoo import api, fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Model"

    name = fields.Char(required=True)
    description = fields.Text()
    expected_price = fields.Float(required=True)
    postcode = fields.Char(required=True)
    date_availability = fields.Date(
        default=lambda self: date.today() + timedelta(days=90),
        required=True,
        copy=False,
    )
    selling_price = fields.Float(copy=False, readonly=True)
    bedrooms = fields.Integer(required=True, default=2)
    living_area = fields.Integer(required=True)
    facades = fields.Integer(required=True)
    garage = fields.Boolean(required=True)
    garden = fields.Boolean(required=True)
    garden_area = fields.Integer(required=True)
    total_area = fields.Float(compute="_compute_total_area", readonly=True)
    garden_orientation = fields.Selection(
        [("north", "North"), ("south", "South"), ("east", "East"), ("west", "West")],
        string="Garden Orientation",
    )

    active = fields.Boolean(default=False)
    state = fields.Selection(
        [
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        string="Status",
        required=True,
        copy=False,
        default="new",
    )

    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer = fields.Many2one("res.partner", string="Buyer")
    salesperson = fields.Many2one(
        "res.users",
        string="Sales Person",
        index=True,
        default=lambda self: self.env.user,
    )
    tags_ids = fields.Many2many("estate.tags", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    best_price = fields.Float(compute="_compute_best_price")

    @api.depends("living_area", "garden", "garden_area")
    def _compute_total_area(self):
        for record in self:
            if not record.garden:
                record.total_area = record.living_area
                record.garden_area = 0
            else:
                record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"), default=0)
