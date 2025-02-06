from dateutil.relativedelta import relativedelta
from odoo import fields, models, api, exceptions
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real estate property details"

    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description", required=True)
    postcode = fields.Char(string="Postcode")
    expected_price = fields.Float("Expected Price")
    date_availability = fields.Date(
        string="Available From",
        copy=False,
        default=fields.Date.today() + relativedelta(months=3),
    )

    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(
        string="Selling Price", required=True, default=0.0, readonly=True, copy=False
    )
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
    )

    active = fields.Boolean(default=True)

    state = fields.Selection(
        string="State",
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        default="new",
        required=True,
        copy=False,
    )

    total_area = fields.Float(string="Total Aream(sqm)", compute="_compute_total_area")
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    user_id = fields.Many2one(
        "res.users", string="Salesperson", default=lambda self: self.env.user
    )
    partner_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")

    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    best_prices = fields.Float(string="Best Offer", compute="_compute_best_offer")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for property in self:
            if property.offer_ids:
                property.best_prices = max(
                    property.offer_ids.mapped("price"), default=0.0
                )
            else:
                property.best_prices = 0.0

    @api.onchange("garden")
    def onchange_check_garden_status(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = "west"

    def action_to_sold_property(self):
        for record in self:
            if record.state == "cancelled":
                raise exceptions.UserError("A cancelled property can not be sold")
            record.state = "sold"
        return True

    def action_to_cancel_property(self):
        for record in self:
            if record.state == "sold":
                raise exceptions.UserError("A sold property can not be cancelled")
            record.state = "cancelled"
        return True

    # Constraint: Selling price cannot be lower than 90% of the expected price
    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        for record in self:
            # Set a default precision for floating point comparisons
            precision = 2

            if not float_is_zero(
                record.expected_price, precision_rounding=precision
            ) and not float_is_zero(record.selling_price, precision_rounding=precision):
                if (
                    float_compare(
                        record.selling_price,
                        record.expected_price * 0.9,
                        precision_rounding=record.expected_price,
                    )
                    < 0
                ):
                    raise exceptions.ValidationError(
                        "The selling price cannot be lower than 90%% of the expected price!"
                    )

    _sql_constraints = [
        (
            "expected_price_positive",
            "CHECK(expected_price > 0)",
            "Expected Price must be strictly positive!",
        ),
        (
            "selling_price_positive",
            "CHECK(selling_price > 0)",
            "Selling Price must be strictly positive!",
        ),
    ]

    
