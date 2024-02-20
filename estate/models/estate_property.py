from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero

class EstateModel(models.Model):
    _name = "estate.property"
    _description = "Estate/Property"

    name = fields.Char(required=True, default="New House")
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    total_area = fields.Integer(compute="_compute_total_area")
    garden_orientation = fields.Selection(
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West")
        ]
    )
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"), 
            ("offer_accepted", "Offer Accepted"), 
            ("sold", "Sold"), 
            ("cancelled", "Cancelled")
        ],
        default="new",
        required=True)
    active = fields.Boolean(default=True)
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson_id = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user)
    property_tags_ids = fields.Many2many("estate.property.tags", string="Property Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="offers")
    best_price = fields.Float(compute="_compute_best_price")

    _sql_constraints = [
        ("check_expected_price",
        "CHECK(expected_price > 0)", 
        "The expected price must be strictly positive"),
        ("check_selling_price",
        "CHECK(selling_price >= 0)",
        "The selling price must be positive"),
    ]

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        for record in self:
            if record.state == "sold" and float_compare(record.selling_price, record.expected_price * .9, precision_rounding=2) < 0:
                raise ValidationError("The selling price cannot be lower than 90% of the expected price")


    @api.depends("garden_area", "living_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends("offer_ids")
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
            self.garden_orientation = ""

    def action_set_sold(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError("Cancelled properties cannot be sold")
            else:
                record.state = "sold"
        return True

    def action_cancel_property(self):
        for record in self:
            record.state = "cancelled"
        return True
