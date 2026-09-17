from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class Property(models.Model):
    _name = "estate.property"
    _description = "Real estate property"
    _order = "id desc"

    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        string="Available From",
        copy=False,
        default=lambda x: fields.Date.add(fields.Date.today(), months=3)
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    faces = fields.Integer(string="Facades")
    has_garage = fields.Boolean(string="Garage")
    has_garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        selection=[
            ("north", "North"),
            ("east", "East"),
            ("south", "South"),
            ("west", "West")
        ]
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        default="new",
        required=True,
        copy=False,
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled")
        ]
    )
    property_type_id = fields.Many2one("estate.property.type", string="Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson_id = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    total_area = fields.Float(compute="_compute_total_area")
    best_price = fields.Float(string="Best Offer", compute="_compute_best_price")

    # Constraints
    _check_expected_price = models.Constraint(
        "CHECK(expected_price > 0)",
        "Expected price must be strictly positive",
    )
    _check_selling_price = models.Constraint(
        "CHECK(selling_price >= 0)",
        "Expected price must be positive",
    )

    @api.depends("garden_area", "living_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price")) if record.offer_ids else 0.0

    @api.constrains("expected_price", "selling_price")
    def _check_expected_price_selling_price(self):
        for record in self:
            if not float_is_zero(record.selling_price, precision_digits=2) and \
                    float_compare(record.expected_price * 0.90, record.selling_price, precision_digits=2) > 0:
                raise ValidationError("Selling price must be above 90% of expected price")

    @api.onchange("has_garden")
    def _onchange_has_garden(self):
        if self.has_garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def unlink(self):
        if self.state not in ("new", "cancelled"):
            raise ValidationError("Can only delete Property that are New or Cancelled")
        return super().unlink()

    def action_do_sold(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError("Canceled property cannot be sold")
            else:
                record.state = "sold"
        return True

    def action_do_cancel(self):
        for record in self:
            if record.state == "sold":
                raise UserError("Sold property cannot be canceled")
            else:
                record.state = "cancelled"
        return True
