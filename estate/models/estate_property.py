from dateutil.relativedelta import relativedelta
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "This is the model for estate property"
    _order = "id desc"

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    postcode = fields.Char(string="PostCode")
    date_availability = fields.Date(
        string="Available From",
        copy=False,
        default=lambda self: fields.Date.today() + relativedelta(months=3),
    )
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False, default=0.0)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area(sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area(sqm)")
    garden_orientation = fields.Selection(
        string="Gardern Orientation",
        selection=[("north", "North"), ("south", "South"), ("east", "East"), ("west", "West")],
    )
    active = fields.Boolean(string="Active", default=True)
    state = fields.Selection(
        string="Status",
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        required=True, default="new", copy=False,
    )
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson_id = fields.Many2one(
        "res.users", string="Salesperson", default=lambda self: self.env.user
    )
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Integer(string="Total Area (sqm)", compute="_compute_total_area")
    best_price = fields.Float(string="Best Offer", compute="_compute_best_price")

    _sql_constraints = [(
        "estate_property_check_expected_price",
        "CHECK(expected_price > 0)",
        "The expected price must be positive",
        ),
        (
            "estate_property_check_selling_price",
            "CHECK(selling_price >= 0)",
            "The selling price must be positive",
    ),]

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price_and_expected_price(self):
        for record in self:
            if (
                not float_is_zero(record.selling_price, precision_digits=2)
                and float_compare(
                    record.selling_price, record.expected_price * 0.9, precision_digits=2
                )
                < 0
            ):
                raise ValidationError(
                    f"The selling price cannot be lower than 90% of the expected price"
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

    def action_estate_property_sold(self):
        for record in self:
            if record.state == "sold":
                raise UserError("This property is already sold")
            if record.state == "cancelled":
                raise UserError("You cannot sell a cancelled property")
            record.state = "sold"

    def action_estate_property_cancel(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError("This property is already cancelled")
            if record.state == "sold":
                raise UserError("You cannot cancel a sold property")
            record.state = "cancelled"

    @api.ondelete(at_uninstall=False)
    def _unlink_if_new_or_cancelled(self):
        for record in self:
            if record.state not in ["new", "cancelled"]:
                raise UserError("You cannot delete a property that is not new or cancelled")
