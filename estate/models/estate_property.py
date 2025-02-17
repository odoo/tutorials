from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _inherit = ["mail.thread"]
    _description = "Real Estate Property"
    _order = "id desc"

    def _default_date_availability(self):
        return datetime.today() + relativedelta(months=3)

    company_id = fields.Many2one(
        "res.company",
        required=True,
        string="Company",
        default=lambda self: self.env.company,
    )
    active = fields.Boolean(default=True)
    name = fields.Char(string="Property Name", required=True, tracking=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postal Code")
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(
        string="Selling Price", readonly=True, copy=False, tracking=True
    )
    bedrooms = fields.Integer(string="Number of Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area")
    facades = fields.Integer(string="Number of Facades")
    garage = fields.Boolean(string="Garage Available")
    garden = fields.Boolean(string="Garden Available")
    garden_area = fields.Integer(string="Garden Area")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
    )
    state = fields.Selection(
        string="Status of Document",
        default="new",
        selection=[
            ("new", "New"),
            ("received", "Received"),
            ("accepted", "Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        store=True,
        tracking=True,
    )
    date_availability = fields.Date(
        string="Available From", copy=False, default=_default_date_availability
    )

    total_area = fields.Float(compute="_compute_total", string="Total Area")
    best_price = fields.Float(compute="_compute_best_price", string="Best Offer")

    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    partner_id = fields.Many2one("res.partner", string="Buyer", copy="False")
    users_id = fields.Many2one(
        "res.users",
        string="Salesman",
        # default=lambda self: self.env.user,
    )

    property_tag_ids = fields.Many2many("estate.property.tag", string="Tags")

    offer_ids = fields.One2many("estate.property.offer", "property_id")

    _sql_constraints = [
        (
            "check_expected_price",
            "CHECK(expected_price > 0)",
            "Expected price always be > 0",
        ),
        (
            "check_selling_price",
            "CHECK(selling_price > 0)",
            "Selling price always be > 0",
        ),
    ]

    @api.depends("garden_area", "living_area")
    def _compute_total(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(offer.price for offer in record.offer_ids)
            else:
                record.best_price = 0.0

    @api.onchange("garden")
    def _comoute_garden(self):
        if self.garden is True:
            self.garden_orientation = "north"
            self.garden_area = 10
        else:
            self.garden_orientation = False
            self.garden_area = 0

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        for record in self:
            if float_is_zero(record.selling_price, precision_digits=2):
                continue
            min_selling_price = record.expected_price * 0.9

            if (
                float_compare(
                    record.selling_price, min_selling_price, precision_digits=2
                )
                < 0
            ):
                raise ValidationError(
                    "Selling price cannot be lower than 90% of expected price"
                )

    @api.ondelete(at_uninstall=False)
    def _unlink_block_offer_deletion(self):
        for record in self:
            if record.state not in ["new", "cancelled"]:
                state_label = dict(self._fields["state"].selection).get(record.state)
                raise UserError(
                    f"This offer is in {state_label} state. You can't delete it."
                )


    def action_sell_property(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError("Cancelled property cannot be sold")

            # Check if there is at least one accepted offer
            has_accepted_offer = any(
                offer.status == "accepted" for offer in record.offer_ids
            )

            print(has_accepted_offer , "============================================") 

            if not has_accepted_offer:
                raise UserError("You cannot sell a property without an accepted offer")

            record.state = "sold"  # Update state only when a valid offer is found

    def mark_offer_cancel(self):
        for record in self:
            if record.state == "sold":
                raise UserError("Sold property can not be Cancelled")
            else:
                record.state = "cancelled"
        return True
