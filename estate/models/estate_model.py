from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "This is a Estate property model containing all the data associated with housing."

    _auto = True
    _log_access = False
    _order = "id desc"
    # _table = "estate.property

    name = fields.Char(string="Name", required=True, index=True)
    description = fields.Text("Description")
    postcode = fields.Char("Postcode")
    date_availability = fields.Date(
        "Available From", copy=False, default=fields.Date.today() + timedelta(days=90)
    )
    expected_price = fields.Float("Expected Price", required=False)
    selling_price = fields.Float("Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer("Total Bedrooms", default=2)
    living_area = fields.Integer("Living Area (sqm)")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage")
    total_area = fields.Integer("Total Area", compute="_compute_total_area")
    best_price = fields.Integer("Best Offer", compute="_compute_best_offer")
    garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden Area (sqms)")
    garden_orientation = fields.Selection(
        string="Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("west", "West"),
            ("east", "East"),
        ],
        help="Type is used to get the garden orientation in a specific direction",
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("new", "New"),
            ("o_received", "Offer Received"),
            ("o_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        copy=False,
        default="new",
    )
    property_type_id = fields.Many2one("estate.property.type", "Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    seller_id = fields.Many2one(
        "res.users",
        string="Salesperson",
        default=lambda self: self.env.user,
    )
    tags_ids = fields.Many2many("estate.property.tag", "Tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    active = fields.Boolean("Active", default=True)

    _check_expected_price = models.Constraint(
        "CHECK (expected_price > 0)",
        "A property expected price must be strictly positive",
    )

    _check_selling_price_positive = models.Constraint(
        "CHECK (selling_price > 0)",
        "A property selling price must be positive",
    )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"), default=0.0)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = None

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        if (
            not float_is_zero(self.selling_price, 2)
            and float_compare(self.selling_price, (self.expected_price * 0.9), 2) == -1
        ):
            raise ValidationError(
                "Selling Price must not be less than 90% of expected price."
            )

    def action_sold_property(self):
        self.ensure_one()
        if self.state == "cancelled":
            raise ValidationError(
                "An estate property cannot be sold which is already marked as cancelled"
            )

        self.state = "sold"

    def action_cancel_property(self):
        self.ensure_one()
        if self.state == "sold":
            raise ValidationError(
                "An estate property cannot be cancel which is already marked as sold"
            )

        self.state = "cancelled"
