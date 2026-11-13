from dateutil.relativedelta import relativedelta
from odoo import api, fields, models
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
        copy=False, default=lambda _: fields.Date.today() + relativedelta(months=3)
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
        copy=False,
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
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
        string="Status",
    )
    property_type_id = fields.Many2one(
        "estate.property.type",
        string="Property Type",
    )
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson_id = fields.Many2one(
        "res.users", string="Salesperson", default=lambda self: self.env.user
    )
    tag_ids = fields.Many2many(
        "estate.property.tag", relation="estate_property_tag_rel", string="Tags"
    )
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="offers")
    total_area = fields.Float(compute="_compute_total_area", store=True)
    best_price = fields.Float(compute="_compute_best_price", store=True)

    _check_price = models.Constraint(
        "check(expected_price > 0 AND selling_price >= 0)",
        "the price should be strictly positive",
    )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            if record.garden:
                record.total_area = record.living_area + record.garden_area
            else:
                record.total_area = record.living_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"), default=0)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_sold(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError("cancelled properties cannot be sold.")
            if record.state == "new":
                raise UserError("offer should be accepted first!")
            record.state = "sold"
        return True

    def action_cancel(self):
        for record in self:
            if record.state == "sold":
                raise UserError("sold properties cannot be cancelled.")
            record.state = "cancelled"
        return True

    @api.constrains("selling_price", "expected_price")
    def check_selling_price(self):
        for record in self:
            if not float_is_zero(record.selling_price, precision_digits=2) and (
                float_compare(
                    record.selling_price,
                    record.expected_price * 0.9,
                    precision_digits=2,
                )
                < 0
            ):
                raise ValidationError(
                    (
                        "the selling price must be atleast 90% of expected price. which is =",
                        record.expected_price,
                    )
                )
