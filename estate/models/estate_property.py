from odoo import fields, models
from odoo.exceptions import UserError
from odoo.orm.models import api
from odoo.tools.date_utils import add


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "An estate property"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False, default=lambda _: add(fields.Date.today(), months=+3)
    )
    expected_price = fields.Integer(required=True)
    selling_price = fields.Integer(
        copy=False, readonly=True, compute="_compute_selling_price"
    )
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        [("north", "North"), ("south", "South"), ("east", "East"), ("west", "West")]
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        [
            ("new", "New"),
            ("received", "Offer Received"),
            ("accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        required=True,
        copy=False,
        default="new",
    )

    # Foreign fields
    property_type_id = fields.Many2one(
        "estate.type", required=True, ondelete="restrict"
    )
    buyer_id = fields.Many2one(
        "res.partner",
        required=False,
        copy=False,
        ondelete="restrict",
        compute="_compute_buyer_id",
    )
    seller_id = fields.Many2one(
        "res.users",
        required=True,
        default=lambda self: self.env.user,
        ondelete="restrict",
    )
    tag_ids = fields.Many2many("estate.tag")
    offer_ids = fields.One2many("estate.offer", "property_id")

    # Computed fields
    total_area = fields.Integer(compute="_compute_total_area")
    best_price = fields.Integer(compute="_compute_best_price")

    @api.depends("offer_ids")
    def _compute_selling_price(self):
        for record in self:
            record.selling_price = None
            for offer in record.offer_ids:
                if offer.status == "accepted":
                    record.selling_price = offer.price
                    break

    @api.depends("offer_ids")
    def _compute_buyer_id(self):
        for record in self:
            record.buyer_id = None
            for offer in record.offer_ids:
                if offer.status == "accepted":
                    record.buyer_id = offer.partner_id
                    break

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            # Fallback to 0 if no records are present
            record.best_price = max(record.offer_ids.mapped("price") + [0])

    @api.onchange("garden")
    def _onchange_garden(self):
        self.garden_area = 10 if self.garden else None
        self.garden_orientation = "north" if self.garden else None

    # Actions

    def set_state_cancel(self):
        for record in self:
            if record.state == "sold":
                raise UserError("A sold property cannot be cancelled")

            record.state = "cancelled"

        return True

    def set_state_sold(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError("A cancelled property cannot be sold")

            record.state = "sold"

        return True
