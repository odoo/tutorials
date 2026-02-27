from datetime import timedelta
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _order = "id desc"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False, default=lambda self: fields.Date.today() + timedelta(days=90)
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
        [
            ('north', "North"),
            ('south', "South"),
            ('east', "East"),
            ('west', "West"),
        ]
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        [
            ('new', "New"),
            ('offer_received', "Offer Received"),
            ('offer_accepted', "Offer Accepted"),
            ('sold', "Sold"),
            ('cancelled', "Cancelled"),
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
    salesperson_id = fields.Many2one(
        "res.users",
        string="Salesperson",
        default=lambda self: self.env.user,
    )
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Float(compute="_compute_total_area", store=True)
    best_price = fields.Float(
        compute="_compute_best_price", string="Best Offer", store=True
    )
    maintanance_req = fields.One2many(
        "estate.property.maintanance", "property_id", string="Maintanace Request"
    )

    _expected_price_check = models.Constraint(
        "CHECK(expected_price > 0)", "The expected price must be strictly positive."
    )
    _selling_price_check = models.Constraint(
        "CHECK(selling_price >= 0)", "The selling price must be positive"
    )

    @api.depends("garden_area", "living_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped("price"))
            else:
                record.best_price = 0

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        for record in self:
            if float_is_zero(record.selling_price, precision_rounding=0.01):
                continue

            min_price = record.expected_price * 0.9

            if float_compare(record.selling_price, min_price, precision_digits=2) < 0:
                raise ValidationError(
                    "The selling price cannot be lower than 90% the expected price."
                )

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    @api.ondelete(at_uninstall=False)
    def _check_state_before_delete(self):
        for record in self:
            if record.state not in ("new", "cancelled"):
                raise UserError("You can only delete New or Cancelled properties.")

    def action_sold(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError(_("A cancelled property cannot be sold."))
            record.state = "sold"
            record.action_archive()
        return True

    def action_cancel(self):
        for record in self:
            if record.state == "sold":
                raise UserError("A sold property cannot be cancelled.")
            record.state = "cancelled"
        return True

    def action_best_offer(self):
        for record in self:
            maxi = -1
            for offer in record.offer_ids:
                if offer.price > maxi:
                    max_record = offer
                    maxi = offer.price

            max_record.action_accept()
