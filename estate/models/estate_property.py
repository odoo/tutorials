from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_is_zero, float_compare


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _order = "id DESC"

    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(string="Available From", copy=False, default=fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        selection=[("north", "North"), ("south", "South"), ("east", "East"), ("west", "West")],
        help="The orientation of the Garden",
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[("new", "New"), ("received", "Offer Received"), ("accepted", "Offer Accepted"), ("sold", "Sold"), ("cancelled", "Cancelled")],
        required=True,
        copy=False,
        default="new",
        help="The current state of the property",
    )
    property_type_id = fields.Many2one("estate.property.type")
    salesperson_id = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", copy=False)
    tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    total_area = fields.Integer(compute="_compute_total_area")
    best_price = fields.Float(string="Best offer", compute="_compute_best_price")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids")
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(self.offer_ids.mapped("price"))
            else:
                record.best_price = 0.0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = ""

    def action_property_sold(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError("Cancelled properties cannot be sold.")
            record.state = "sold"
        return True

    def action_property_cancel(self):
        for record in self:
            if record.state == "sold":
                raise UserError("Sold properties cannot be cancelled.")
            record.state = "cancelled"
        return True

    _positive_expected_price = models.Constraint(
        "CHECK(expected_price > 0)",
        "The expected price must be strictly positive.",
    )

    @api.constrains("selling_price", "expected_price")
    @api.onchange("selling_price", "expected_price")
    def _check_ninety_percent(self):
        for record in self:
            if not float_is_zero(record.selling_price, 2) and float_compare(record.expected_price * 0.9, record.selling_price, 2) == 1:
                raise ValidationError("The selling price must be at least 90% of the expected price! You must reduce the expected price if you want to accept this offer.")
