from odoo import api, fields, models
from odoo.exceptions import ValidationError, UserError
from dateutil.relativedelta import relativedelta
from odoo.tools import float_compare, float_is_zero


class PropertyPlan(models.Model):
    _name = "estate.property"
    _description = "Estate property tables"
    _order = "id desc"
    _inherit = ["mail.thread"]

    name = fields.Char(string="Title", required=True, tracking=True)
    description = fields.Text(string="Description", tracking=True)
    postcode = fields.Char(string="Postcode", tracking=True)
    date_availability = fields.Date(
        string="Available From",
        copy=False,
        default=(fields.Date.today() + relativedelta(months=+3)),
        tracking=True,
    )
    expected_price = fields.Float(string="Expected Price", required=True, tracking=True)
    selling_price = fields.Float(string="Selling Price", readonly=True, tracking=True)
    bedrooms = fields.Integer(string="Bedrooms", default=2, tracking=True)
    living_area = fields.Integer(string="Living Area (sqm)", tracking=True)
    facades = fields.Integer(string="Facades", tracking=True)
    garage = fields.Boolean(string="Garage", tracking=True)
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)")
    active = fields.Boolean(string="Active", default=True)
    state = fields.Selection(
        string="State",
        default="new",
        copy=False,
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        help="Sate of Offer",
        tracking=True,
    )
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
        help="Used to decide the direction of Garden",
        tracking=True,
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type", tracking=True)
    tag_ids = fields.Many2many("estate.property.tag", string="Property Tag")
    partner_id = fields.Many2one("res.partner", string="Buyer", copy=False, tracking=True)
    sales_person = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user)
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Price")
    total_area = fields.Float(string="Total Area (sqm)", compute="_compute_total_area")
    best_price = fields.Float(string="Best Offer", compute="_compute_best_price")
    priority = fields.Integer(default=1)
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        required=True,
        default=lambda self: self.env.company,
    )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped("price"))
            else:
                record.best_price = 0.0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 00
            self.garden_orientation = ""

    def action_property_cancelled(self):
        if self.state == "sold":
            raise ValidationError("Cannot cancel a sold property!")
        else:
            self.state = "cancelled"
        return True

    def action_property_sold(self):
        if self.state == "cancelled":
            raise ValidationError("Cannot sell a cancelled property!")
        else:
            self.state = "sold"
        return True

    _sql_constraints = [
        (
            "check_expected_price",
            "CHECK(expected_price > 0)",
            "Expected price must be strictly positive!",
        ),
        (
            "check_selling_price",
            "CHECK(selling_price >= 0)",
            "Selling price must be positive!",
        ),
    ]

    @api.constrains("selling_price", "expected_price")
    def check_selling_price(self):
        for price in self:
            if float_is_zero(price.selling_price, 2) != 1:
                if (
                    float_compare(price.expected_price * 0.9, price.selling_price, 2)
                    == 1
                ):
                    raise ValidationError(
                        "The selling price must be at least 90% of the expected price!You must reduce the expected price if you want to accept this offer."
                    )

    @api.ondelete(at_uninstall=False)
    def _unlink_if_state_new_cancelled(self):
        if self.state != "new" and self.state != "cancelled":
            raise UserError("Only new and cancelled properties can be deleted!")
