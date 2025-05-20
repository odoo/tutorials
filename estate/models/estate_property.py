from dateutil.relativedelta import relativedelta

from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _order = "id desc"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    # Basic Fields
    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    # Date Fields
    date_availability = fields.Date(
        string="Available From",
        copy=False,
        default=lambda self: fields.Date.today() + relativedelta(months=3)
    )
    # Price Fields
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    # Property Details
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Float(string="Living Area (sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Float(string="Garden Area (sqm)")
    best_price = fields.Float("Best Offer", compute="_compute_best_price", store=True)
    # Selection Fields
    garden_orientation = fields.Selection([('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')], string='Garden Orientation')
    state = fields.Selection(
        [
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled"),
        ],
        string="Status",
        required=True,
        copy=False,
        default="new",
    )
    active = fields.Boolean(string="Active", default=True)
    # Many2one, Many2many, One2many Relation to Property Type
    property_type_id = fields.Many2one('estate.property.type', string="Property Type", required=True)
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson_id = fields.Many2one(
        "res.users",
        string="Sales Person",
        default=lambda self: self.env.user,
        required=True,
    )
    offer_ids = fields.One2many(
    "estate.property.offer",
    "property_id",
    string="Offers"
    )
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    total_area = fields.Float(string='Total Area (sqm)', compute='_compute_total_area', store=True, help='Sum of living area and garden area')
    company_id = fields.Many2one(
        'res.company', 
        string='Company', 
        required=True, 
        default=lambda self: self.env.company
    )
    # SQL Constraints
    _sql_constraints = [
        (
            "check_expected_price_positive",
            "CHECK(expected_price >= 0)",
            "The expected price must be strictly positive.",
        ),
        (
            "check_selling_price_positive",
            "CHECK(selling_price >= 0)",
            "The selling price must be strictly positive.",
        ),
        (
            "check_bedrooms_positive",
            "CHECK(bedrooms >= 0)",
            "The number of bedrooms must be zero or positive.",
        ),
    ]
    # Computed Fields & Onchange

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.offer_price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("offer_price"), default=0.0)

    # Onchange
    @api.onchange('garden')
    def _onchange_garden(self):
        for record in self:
            if record.garden:
                record.garden_area = 10
                record.garden_orientation = 'north'
            else:
                record.garden_area = 0
                record.garden_orientation = False
           
    # Add Action Logic of "Cancel" & "Sold"
    def action_set_sold(self):
        for record in self:
            if record.state == "canceled":
                raise UserError("A cancelled property cannot be sold.")

            if record.state != "offer_accepted":
                raise UserError(
                    "You cannot mark a property as sold without accepting an offer."
                )

            record.state = "sold"

        return True

    def action_set_canceled(self):
        for record in self:
            if record.state == "sold":
                raise UserError("Sold property cannot be canceled.")
            record.state = "canceled"

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if float_is_zero(record.selling_price, precision_digits=2):
                continue
            min_acceptable_price = 0.9 * record.expected_price
            if float_compare(record.selling_price, min_acceptable_price, precision_digits=2) < 0:
                raise ValidationError("The selling price cannot be lower than 90% of the expected price.")

    @api.ondelete(at_uninstall=False)
    def _check_state_before_delete(self):
        for record in self:
            if record.state not in ('new', 'canceled'):
                raise UserError("You can only delete properties in 'New' or 'canceled' state.")
