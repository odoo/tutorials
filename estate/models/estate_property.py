from datetime import timedelta

from odoo import api, exceptions, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property Name"
    _order = "id desc"
    _inherit = ["mail.thread"]
    
    name = fields.Char("Property Name", required=True)
    description = fields.Text("Description")
    postcode = fields.Char("Postcode", size=6, tracking=True)
    date_availability = fields.Date(
        "Date Availability",
        copy=False,
        default=lambda self: fields.Date.today() + timedelta(days=90),
    )
    expected_price = fields.Float("Expected Price", required=True)
    selling_price = fields.Float(
        "Selling Price",
        readonly=True,
        copy=False,
    )
    bedrooms = fields.Integer("Bedrooms", default=2)
    living_area = fields.Integer("Living Area(sqm)")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden Area(sqm)", default=0)
    total_area = fields.Integer(
        "Total Area (sqm)", compute="_compute_total_area", store=True
    )
    garden_orientation = fields.Selection(
        string="Type",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
    )
    active = fields.Boolean("Active", default=True, help="if you want to active")
    state = fields.Selection(
        required=True,
        copy=False,
        default="new",
        selection=[
            ("new", "New"),
            ("offer received", "Offer Received"),
            ("offer accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
    )
    salesman_id = fields.Many2one(
        "res.users", default=lambda self: self.env.user, string="Salesman"
    )
    partner_id = fields.Many2one("res.partner", string="Partner", copy=True)
    tags_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    best_price = fields.Float(
        string="Best Offer", compute="_compute_best_price", store=True
    )
    property_type_id = fields.Many2one("estate.property.types", string="Property Type")
    company_id = fields.Many2one(
        "res.company",
        required=True,
        default=lambda self: self.env.company,
        string="Company"
    )

    _sql_constraints = [
        (
            "check_expected_price",
            "CHECK(expected_price > 0)",
            "The expected price must be strictly positive.",
        ),
        (
            "check_selling_price",
            "CHECK(selling_price >= 0)",
            "The selling price must be positive.",
        ),
    ]

    # computed fields
    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"), default=0.0)

    # onchange
    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    # Constaints
    @api.constrains("offer_ids")
    def _check_offer_price(self):
        for record in self:
            for offer in record.offer_ids:
                if offer.price < 0:
                    raise ValidationError("The offer price must be positive")

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        for record in self:
            # check if selling_price is zero
            if float_is_zero(record.selling_price, precision_rounding=0.01):
                continue
            # selling_price is at least 90% of expected_price
            if (
                float_compare(
                    record.selling_price, (record.expected_price*0.9), precision_rounding=2
                )
                < 0
            ):
                raise ValidationError(
                    "The selling price cannot be less than 90% of the expected price."
                )

    @api.ondelete(at_uninstall=False)
    def _check_delete_state(self):
        for record in self:
            if record.state not in ["New", "Cancelled"]:
                raise exceptions.UserError(
                    "You cannot delete a property unless its state is 'New' or 'Cancelled'."
                )

    # function for Sold and Cancelled Button
    def action_set_status_sold(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError("Cancelled Property cannot be Sold")
            elif not record.offer_ids.filtered(
                lambda offer: offer.status == "accepted"
            ):
                raise UserError("No offer is accepted")
            elif record.state != "cancelled":
                record.state = "sold"
            else:
                raise UserError("It is already sold")
        return True

    def action_set_status_cancel(self):
        for record in self:
            if record.state == "sold":
                record.state = "cancelled"
            elif record.state == "sold":
                raise UserError("It cannot be canceled once sold")
            elif record.state == "cancelled":
                raise UserError("It is already canceled")
        return True
