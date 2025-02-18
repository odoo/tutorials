from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.tools.float_utils import float_compare, float_is_zero
from odoo.exceptions import UserError, ValidationError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _inherit = ["mail.thread"]
    _order = "id desc"

    _sql_constraints = [
        (
            "expected_price",
            "CHECK(expected_price > 0)",
            "Expected Price should be positive",
        ),
        (
            "selling_price_constraint",
            "CHECK(selling_price >= 0)",
            "Selling Price should be positive",
        ),
    ]

    active = fields.Boolean(string="Active", default=True)
    name = fields.Char(required=True)
    description = fields.Text("Description")
    postcode = fields.Text(string="Postcode", tracking=True)
    selling_price = fields.Float(string="Selling Price", default=0.0, readonly=True)
    expected_price = fields.Float(string="Expected Price")
    best_price = fields.Float("Best Price", compute="_compute_best_price")
    bedrooms = fields.Integer(string="Number of Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area (m²)")
    facades = fields.Integer(string="Number of Facades")
    garage = fields.Boolean(string="Has Garage")
    garden = fields.Boolean(string="Has Garden", default=True)
    garden_area = fields.Integer(string="Garden Area (m²)", default=False)
    date_availability = fields.Date(
        string="Date Availability", default=datetime.today() + relativedelta(months=3)
    )
    status = fields.Selection(
        [
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        string="Status",
        default="new",
        tracking=True,
    )
    garden_orientation = fields.Selection(
        [
            ("north", "North"),
            ("east", "East"),
            ("west", "West"),
            ("south", "South"),
        ],
        string="Garden Orientation",
    )
    total_area = fields.Float("Total Area", compute="_compute_total_area")

    property_type_id = fields.Many2one(
        comodel_name="property.type", string="Property Type"
    )
    tags_ids = fields.Many2many(comodel_name="property.tag", string="Property Tags")
    buyer_id = fields.Many2one(comodel_name="res.partner", string="Buyer")
    seller_id = fields.Many2one(
        comodel_name="res.users",
        string="Salesperson",
        default=lambda self: self.env.user,
    )
    offer_ids = fields.One2many(
        comodel_name="estate.property.offer",
        inverse_name="property_id",
        string="Offer Id",
    )

    company_id = fields.Many2one(
        "res.company",
        string="Company",
        required=True,
        default=lambda self: self.env.user.company_id,
    )

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"), default=0.0)

    @api.depends("garden_area", "living_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.constrains("selling_price", "expected_price")
    def check_price(self):
        for record in self:
            # skip validation if selling price is 0 (unvalidated offer)
            if float_is_zero(record.selling_price, precision_digits=2):
                continue
            min_selling_price = record.expected_price * 0.9

            if (
                float_compare(
                    record.selling_price, min_selling_price, precision_digits=2
                )
                == -1
            ):
                raise ValidationError(
                    "Selling Price cannot be lower than 90 percent of expected price"
                )

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = False
            self.garden_orientation = False

    @api.ondelete(at_uninstall=False)
    def ondelete(self):
        for record in self:
            if record.status not in ["new", "cancelled"]:
                raise UserError(
                    "You can only delete records with state New or cancelled"
                )

    def action_cancel(self):
        for record in self:
            if record.status == "sold":
                raise UserError("A sold property cannot be cancelled!")
            record.status = "cancelled"

    def action_sold(self):
        for record in self:
            if record.status == "cancelled":
                raise UserError("It cannot be sold once cancelled")
            elif not record.offer_ids.filtered(lambda offer: offer.state == "accepted"):
                raise UserError("No offer is accepted")
            elif record.status != "cancelled":
                record.status = "sold"
            else:
                raise UserError("It is already sold")
        return True
