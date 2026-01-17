from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _order = "id desc"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()

    date_availability = fields.Date(
        copy=False,
        default=lambda self: fields.Date.today() + relativedelta(months=3),
    )

    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[
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
        required=True,
        copy=False,
        default="new",
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one(
        "res.partner",
        string="Buyer",
        copy=False,
    )
    user_id = fields.Many2one(
        "res.users", string="Salesman", default=lambda self: self.env.user
    )
    tag_ids = fields.Many2many(
        "estate.property.tag",
        string="Tags",
    )
    offer_ids = fields.One2many(
        "estate.property.offer",
        "property_id",
        string="Offers",
    )
    salesperson_id = fields.Many2one(
        "res.users", string="Salesperson", default=lambda self: self.env.user
    )
    total_area = fields.Float(
        compute="_compute_total_area", string="Total Area", readonly=False
    )
    best_price = fields.Float(
        compute="_compute_best_price", string="Best Offer", store=True
    )
    _check_expected_price = models.Constraint(
        "CHECK(expected_price > 0)",
        "The expected price must be strictly positive",
    )
    _check_selling_price = models.Constraint(
        "CHECK(selling_price >= 0)", "The selling price must be positive"
    )

    @api.ondelete(at_uninstall=False)
    def _unlink_if_allowed(self):
        for record in self:
            if record.state not in ("new", "cancelled"):
                raise ValidationError(
                    _("You can only delete properties that are New or Cancelled.")
                )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"), default=0.0)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"

        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_sold(self):
        if self.filtered(lambda x: x.state == "cancelled"):
            raise UserError(_("A cancelled Property cannot be sold."))
        self.write({"state": "sold"})

    def action_cancel(self):
        if self.filtered(lambda x: x.state == "sold"):
            raise UserError(_("A sold Property cannot be cancelled."))
        self.write({"state": "cancelled"})

    @api.constrains("expected_price", "selling_price")
    def _check_selling_price(self):
        for record in self:
            if float_is_zero(record.selling_price, precision_rounding=0.01):
                continue
            min_price = record.expected_price * 0.9
            if float_compare(record.selling_price, min_price, precision_rounding=0.01) < 0:
                raise ValidationError("The selling price cannot be lower than 90% of the expected price.")

    def accept_best_price(self):
        for record in self:
            if not record.offer_ids:
                raise UserError("There are no offers to accept.")

            best_offer = max(record.offer_ids, key=lambda t: t.price)
            record.offer_ids.write({"status": "refused"})
            best_offer.write({"status": "accepted"})

            record.selling_price = record.best_price
            record.buyer_id = best_offer.partner_id
        return True
