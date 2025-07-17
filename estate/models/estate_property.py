from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, _
from odoo.tools.float_utils import float_compare, float_is_zero
from odoo.exceptions import UserError, ValidationError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _order = "id desc"

    _sql_constraints = [
        (
            "_check_expected_price",
            "CHECK(expected_price > 0)",
            "The expected price must be positive.",
        ),
        (
            "_check_selling_price",
            "CHECK(selling_price >= 0)",
            "The selling price must be positive.",
        ),
    ]

    name = fields.Char(required=True, string="Title")
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(
        default=lambda self: fields.Date.today() + relativedelta(months=3),
        copy=False,
        string="Available From",
    )
    expected_price = fields.Float(required=True, string="Expected Price")
    selling_price = fields.Float(readonly=True, copy=False, string="Selling Price")
    bedrooms = fields.Integer(default=2, string="Bedrooms")
    living_area = fields.Integer(string="Living Area (sqm)")
    total_area = fields.Float(compute="_compute_total_area", store=True, string="Total Area")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)")
    active = fields.Boolean(default=True, string="Active")
    garden_orientation = fields.Selection(
        [("north", "North"), ("south", "South"), ("east", "East"), ("west", "West")],
        string="Garden Orientation",
    )
    state = fields.Selection([("new", "New"), ("offer_received", "Offer Received"), ("offer_accepted", "Offer Accepted"), ("sold", "Sold"), ("cancelled", "Cancelled")], required=True, copy=False, default="new", string="State")
    property_type_id = fields.Many2one("estate.property.types", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson_id = fields.Many2one(
        "res.users", string="Salesperson", default=lambda self: self.env.user
    )
    tag_ids = fields.Many2many("estate.property.tags", string="Tags")

    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    best_price = fields.Float(compute="_get_best_offer_price", store=True, string="Best Price")

    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)

    @api.ondelete(at_uninstall=False)
    def _unlink_except_state_new_or_cancelled(self):
        for record in self:
            if record.state not in ["new", "cancelled"]:
                raise UserError(_("You can only delete properties in 'New' or 'Cancelled' state."))

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _get_best_offer_price(self):
        for record in self:
            prices = record.offer_ids.mapped("price")
            record.best_price = max(prices) if prices else 0.0

    @api.onchange("garden")
    def _onchange_garden(self):
        for record in self:
            if record.garden:
                record.garden_area = 10
                record.garden_orientation = "north"
            else:
                record.garden_area = 0
                record.garden_orientation = False

    def action_set_state_sold(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError(_("Cancelled property cannot be sold."))
            if not record.offer_ids.filtered(lambda o: o.status == "accepted"):
                raise UserError(_("You cannot sell a property without an accepted offer."))
            record.state = "sold"
        return True

    def action_set_state_cancel(self):
        for record in self:
            if record.state == "sold":
                raise UserError(_("Sold property cannot be cancelled."))
            else:
                record.state = "cancelled"
        return True

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        for record in self:
            if not float_is_zero(record.selling_price, precision_digits=2):
                if float_compare(record.selling_price, record.expected_price * 0.9, precision_digits=2) < 0:
                    raise ValidationError(_("The selling price cannot be lower than 90% of the expected price"))
