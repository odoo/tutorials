from odoo.orm.utils import ValidationError
from odoo.tools import float_compare, float_is_zero

from odoo import api, exceptions, fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _order = "id desc"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False,
        default=lambda self: fields.Date.add(fields.Date.today(), months=3),
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(
        readonly=True,
        copy=False,
        compute="_compute_selling_price",
        store=True,
    )
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[
            ("north", "North"),
            ("east", "East"),
            ("south", "South"),
            ("west", "West"),
        ],
    )
    active = fields.Boolean(default=True)
    stage = fields.Selection(
        [
            ("new", "New"),
            ("offer_received", "Offer received"),
            ("offer_accepted", "Offer accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        required=True,
        copy=False,
        default="new",
        string="Status",
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one(
        "res.partner",
        string="Buyer",
        compute="_compute_buyer_id",
        store=True,
    )
    salesman_id = fields.Many2one(
        "res.users",
        string="Salesman",
        default=lambda self: self.env.user,
    )
    tag_ids = fields.Many2many("estate.property.tag", string="Property Tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Integer(compute="_compute_total_area", string="Total Area")
    best_price = fields.Float(compute="_compute_best_price", string="Best Offer")

    _positive_expected_price = models.Constraint(
        "CHECK(expected_price > 0)",
        "The expected price of a real estate property should be above zero.",
    )
    _positive_selling_price = models.Constraint(
        "CHECK(selling_price >= 0)",
        "The expectsellinged price of a real estate property should be above zero.",
    )

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped("price"))
            else:
                record.best_price = 0

    @api.depends("offer_ids.status", "offer_ids.price")
    def _compute_selling_price(self):
        for record in self:
            if record.offer_ids and "accepted" in record.offer_ids.mapped("status"):
                for offer in record.offer_ids:
                    if offer.status == "accepted":
                        record.selling_price = offer.price
            else:
                record.selling_price = None

    @api.depends("offer_ids.partner_id", "offer_ids.status")
    def _compute_buyer_id(self):
        for record in self:
            if record.offer_ids and "accepted" in record.offer_ids.mapped("status"):
                for offer in record.offer_ids:
                    if offer.status == "accepted":
                        record.buyer_id = offer.partner_id
            else:
                record.buyer_id = None

    @api.depends("garden_area", "living_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        for record in self:
            if (
                not float_is_zero(record.selling_price, precision_digits=2)
                and float_compare(
                    record.selling_price,
                    0.90 * record.expected_price,
                    precision_digits=2,
                )
                == -1
            ):
                raise exceptions.ValidationError(
                    "Selling price cannot be lower than 90% of the expected price.",
                )

    @api.constrains("stage")
    def _check_accepted_offer_when_sold(self):
        for record in self:
            if record.stage == "sold":
                if record.offer_ids and "accepted" in record.offer_ids.mapped("status"):
                    pass
                else:
                    raise exceptions.ValidationError(
                        "Cannot sell a property with no accepted offers on it."
                    )

    @api.constrains("garden")
    def _check_garden_props(self):
        for record in self:
            if not record.garden and (
                record.garden_orientation or record.garden_area != 0
            ):
                raise ValidationError(
                    "Garden Orientation and garden area cannot have values when garden is unchecked."
                )

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_orientation = "north"
            self.garden_area = 10
        else:
            self.garden_orientation = False
            self.garden_area = 0

    @api.ondelete(at_uninstall=False)
    def _unlink_if_new_or_cancelled(self):
        for record in self:
            if record.stage not in ("new", "cancelled"):
                raise exceptions.UserError(
                    "You cannot delete a property that is not new or cancelled.",
                )

    def action_sell(self):
        if any(record.stage == "cancelled" for record in self):
            raise exceptions.UserError("Cancelled properties cannot be sold.")
        self.stage = "sold"
        return True

    def action_cancel(self):
        if any(record.stage == "sold" for record in self):
            raise exceptions.UserError("Sold properties cannot be cancelled.")
        self.stage = "cancelled"
        return True
