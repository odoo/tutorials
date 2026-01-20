from odoo import models, fields, api
from odoo.tools.date_utils import add
from odoo.tools.float_utils import float_compare
from odoo.exceptions import UserError, ValidationError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate properties"
    _order = "id desc"
    _check_expected_price = models.Constraint(
        "CHECK(expected_price > 0)",
        "The expected price must be strictly positive",
    )
    _check_selling_price = models.Constraint(
        "CHECK(selling_price > 0)",
        "The selling price must be strictly positive",
    )

    def _default_availability_date(*args):
        return add(fields.Date.today(), months=3)

    name = fields.Char("Title", required=True)
    description = fields.Text("Description")
    postcode = fields.Char("Postcode")
    date_availability = fields.Date(
        "Available From",
        copy=False,
        default=_default_availability_date,
    )
    expected_price = fields.Float("Expected Price", required=True)
    selling_price = fields.Float("Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer("Bedrooms", default=2)
    living_area = fields.Integer("Living Area (sqm)")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden Area (sqm)")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
        help="Select the direction in which the garden is facing",
    )
    active = fields.Boolean("Active", default=True)
    state = fields.Selection(
        string="Status",
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
    property_type_id = fields.Many2one(
        "estate.property.type", string="Property Type", required=True
    )
    salesperson_id = fields.Many2one(
        "res.users", string="Salesman", default=lambda self: self.env.user
    )
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many(
        comodel_name="estate.property.offer",
        inverse_name="property_id",
        string="Offers",
    )
    total_area = fields.Integer(
        "Total Area (sqm)",
        compute="_compute_total_area",
    )
    best_price = fields.Float("Best Offer", compute="_compute_best_price")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = (
                max(record.offer_ids.mapped("price")) if record.offer_ids else 0
            )

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = None

    def action_sell_property(self):
        if self.state == "cancelled":
            raise UserError("Cancelled properties cannot be sold")

        self.state = "sold"
        return True

    def action_cancel_property(self):
        if self.state == "sold":
            raise UserError("Sold properties cannot be cancelled")
        self.state = "cancelled"
        return True

    @api.constrains("expected_price")
    def _check_expected_price(self):
        for property in self:
            # todo this is not very performant, look for a more efficient way
            for offer in property.offer_ids:
                if (
                    offer.status == "accepted"
                    and float_compare(
                        offer.price,
                        0.9 * property.expected_price,
                        precision_digits=1,
                    )
                    == -1
                ):
                    raise ValidationError(
                        "The selling price must be at least 90% of the expected price! You've already accepted an offer for lower than 90% of the expected price you've entered."
                    )

    @api.ondelete(at_uninstall=False)
    def _unlink_if_state_is_not_new_or_cancelled(self):
        if any(property.state not in ["new", "cancelled"] for property in self):
            raise UserError("Only new and cancelled properties can be deleted")
