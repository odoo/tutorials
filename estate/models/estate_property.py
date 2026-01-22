from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _order = "id desc"

    name = fields.Char(string="Name", required=True)
    postcode = fields.Char(string="Postcode")
    available_from = fields.Date(
        string="Available From",
        copy=False,
        default=fields.Date.add(fields.Date.today(), months=3),
    )

    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True)

    description = fields.Text(string="Description")
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        [
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
        string="Garden Orientation",
    )
    total_area = fields.Integer(
        string="Total Area (sqm)",
        compute="_compute_total_area",
        readonly=True,
    )
    active = fields.Boolean(string="Active", default=True)
    state = fields.Selection(
        [
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled"),
        ],
        string="State",
        default="new",
        required=True,
    )

    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    salesman_id = fields.Many2one(
        "res.users",
        string="Salesman",
        index=True,
        default=lambda self: self.env.user,
    )
    buyer_id = fields.Many2one("res.partner", string="Buyer", index=True)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    best_offer = fields.Float(string="Best Offer", compute="_compute_best_offer")

    _positive_selling_price = models.Constraint(
        "CHECK (selling_price > 0)",
        "Selling price must be positive",
    )

    _positive_expected_price = models.Constraint(
        "CHECK (expected_price > 0)",
        "Expected price must be positive",
    )

    @api.ondelete(at_uninstall=False)
    def _unlink_if_state_is_new_or_canceled(self):
        if any(state not in ("new", "canceled") for state in self.mapped("state")):
            raise UserError(
                "Only properties in 'New' or 'Canceled' state can be deleted.",
            )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for record in self:
            record.best_offer = (
                max(record.offer_ids.mapped("price")) if record.offer_ids else 0.0
            )

    @api.onchange("garden")
    def _onchange_garden(self):
        if not self.garden:
            self.garden_area = 0
            self.garden_orientation = False
        else:
            self.garden_area = 10
            self.garden_orientation = "north"

    @api.constrains("selling_price")
    def _constrains_selling_price(self):
        for record in self:
            if not float_is_zero(record.selling_price, precision_digits=2):
                if float_compare(record.selling_price, record.expected_price * 0.9, precision_digits=2) < 0:
                    raise UserError("Selling price must be at least 90% of the expected price")

    def action_cancel(self):
        for record in self:
            if record.state == "sold":
                message = "Sold properties cannot be canceled"
                raise UserError(message)
            record.state = "canceled"

    def action_sold(self):
        for record in self:
            if record.state == "canceled":
                message = "Canceled properties cannot be sold"
                raise UserError(message)
            record.state = "sold"
        return True
