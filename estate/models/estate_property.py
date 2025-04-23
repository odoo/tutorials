from dateutil import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate: Property"

    name = fields.Char("Title", required=True)
    active = fields.Boolean("Active", default=True)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")

    # Header
    postcode = fields.Char("Postcode")
    date_availability = fields.Date(
        "Availability Date",
        copy=False,
        default=(lambda _: fields.Date.today() + relativedelta.relativedelta(months=3)),
    )
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        required=True,
        copy=False,
        default="new",
    )
    expected_price = fields.Float("Expected Price", required=True, default=0.0)
    selling_price = fields.Float("Selling Price", readonly=True, copy=False)
    best_price = fields.Float("Best Price", compute="_compute_best_price")

    # Description
    bedrooms = fields.Integer("# of bedrooms", default=2)
    living_area = fields.Integer("living area")
    facades = fields.Integer("# of facades")
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    description = fields.Text("Description")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden Area")
    garden_orientation = fields.Selection(
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
    )
    total_area = fields.Float(compute="_compute_total_area")

    # Offers
    offer_ids = fields.One2many(
        "estate.property.offer",
        "property_id",
        string="Offers",
    )

    # Other Info
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesman_id = fields.Many2one(
        "res.users",
        string="Salesperson",
        default=lambda self: self.env.user,
    )

    @api.depends("garden_area", "living_area")
    def _compute_total_area(self) -> None:
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends("offer_ids")
    def _compute_best_price(self) -> None:
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price")) if record.offer_ids else 0.0

    @api.onchange("garden")
    def _onchange_change(self) -> None:
        self.write(
            {
                "garden_area": 10 if self.garden else 0,
                "garden_orientation": "north" if self.garden else None,
            }
        )

    def action_cancel_property(self) -> bool:
        for record in self:
            if record.state != "sold":
                record.state = "cancelled"
            else:
                raise UserError("Cannot cancel a sold property")
        return True

    def action_sold_property(self) -> bool:
        for record in self:
            if record.state != "cancelled":
                record.state = "sold"
            else:
                raise UserError("Cannot sold a cancel property")
        return True
