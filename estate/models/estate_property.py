from dateutil import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate: Property"
    _order = "id desc"

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

    _sql_constraints = [
        (
            "check_property_prices",
            "CHECK(expected_price >= 0 AND selling_price > 0)",
            "A property expected price and selling price must be positive",
        )
    ]

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

    @api.constrains("selling_price")
    def _check_selling_price(self) -> None:
        for record in self:
            if (
                record.offer_ids.filtered(lambda x: x.status == "accepted")
                and float_compare(record.selling_price, 0.9 * record.expected_price, precision_digits=3) == -1
            ):
                raise ValidationError("The selling price should be atleast 90% of the expected price")

    @api.ondelete(at_uninstall=False)
    def _unlink_if_new_or_cancelled(self) -> None:
        if any(record.state not in ("new", "cancelled") for record in self):
            raise UserError("Can't delete an active property")

    def action_cancel_property(self) -> bool:
        if "sold" in self.mapped("state"):
            raise UserError("Cannot cancel a sold property")
        self.write({"state": "cancelled"})
        return True

    def action_sold_property(self) -> bool:
        if "cancelled" in self.mapped("state"):
            raise UserError("Cannot sell a cancel property")
        self.write({"state": "sold"})
        return True
