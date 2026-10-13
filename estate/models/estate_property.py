from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_is_zero
from odoo.tools.float_utils import float_compare


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _order = "id desc"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    name = fields.Char(required=True, default="Unknown")
    property_type_id = fields.Many2one("estate.property.type", string="Type")
    description = fields.Text()
    tag_ids = fields.Many2many("estate.property.tags", string="Tags")
    salesman_id = fields.Many2one("res.users", default=lambda self: self.env.user.id)
    buyer_id = fields.Many2one(
        "res.partner", default=lambda self: self.env.user.id, copy=False
    )
    postcode = fields.Char()
    date_availability = fields.Date(copy=False)
    expected_price = fields.Float(required=True, default=15.6, tracking=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    total_area = fields.Float(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_price")
    garden_orientation = fields.Selection(
        [
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
        string="Garden Orientation",
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        [
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        copy=False,
        default="new",
        tracking=True,
    )
    offer_ids = fields.One2many(
        "estate.property.offers", "property_id", string="Offers"
    )
    _check_expected_price = models.Constraint(
        "CHECK(expected_price > 0)", "Expected price must be positive."
    )
    _check_selling_price_positive = models.Constraint(
        "CHECK(selling_price > 0)", "Property selling price must be positive."
    )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = (
                    record.living_area + record.garden_area
            )

    @api.depends("offer_ids")
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
            self.garden_orientation = ""

    @api.constrains("expected_price", "selling_price")
    def _check_selling_price(self):
        if not float_is_zero(self.selling_price, 2):
            if float_compare(self.selling_price, (self.expected_price * 0.9), 2) == -1:
                raise ValidationError(
                    "Selling Price must not be less than 90% of expected price."
                )

    @api.ondelete(at_uninstall=True)
    def _unlink_if_new_or_cancelled(self):
        for property in self:
            if property.state not in ["cancelled", "new"]:
                raise UserError("Only new and cancelled properties can be deleted.")

    def action_sold(self):
        for property in self:
            if property.state == "new":
                raise UserError("Create a offer to accept and sell the property")
            elif property.state == "cancelled":
                raise UserError("Cancelled Properties Cannot be Sold")
            elif property.state == "offer_accepted":
                property.state = "sold"
                return True
            else:
                raise UserError("Please accept offer to sell a property")

        return False

    def action_cancel(self):
        for property in self:
            if property.state == "sold":
                raise UserError("Sold Properties cannot be Cancelled")
            else:
                property.state = "cancelled"

            property.offer_ids.status = "refused"
        return True
