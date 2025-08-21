from datetime import timedelta
from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError
from odoo.tools import float_is_zero, float_compare


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _order = "id desc"

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    active = fields.Boolean(
        string="Active",
        default=True,
        help="Mark as active if you want the property to be listed.",
    )
    postcode = fields.Char(string="Postcode")
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    date_availability = fields.Date(
        string="Available From",
        default=fields.Date.today() + timedelta(days=90),
        copy=False,
    )
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
    )
    total_area = fields.Integer(
        string="Total Area (sqm)",
        compute="_compute_total_area",
    )
    state = fields.Selection(
        string="State",
        required=True,
        default="new",
        copy=False,
        selection=[
            ("new", "New"),
            ("offer received", "Offer Received"),
            ("offer accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
    )
    salesman_id = fields.Many2one(
        "res.users", string="Salesman", default=lambda self: self.env.user
    )
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False, readonly=True)
    tag_ids = fields.Many2many(
        "estate.property.tag",
        string="Tags",
        help="Properties associated with this tag.",
    )
    offer_ids = fields.One2many(
        "estate.property.offer",
        "property_id",
        string="Offers",
        help="Offers made on this property.",
    )
    best_price = fields.Float(
        string="Best Offer",
        compute="_compute_best_price",
    )
    
    _sql_constraints = [
        (
            "check_expected_price",
            "CHECK(expected_price > 0)",
            "The expected price must be greater than 0.",
        ),
    ]

    @api.ondelete(at_uninstall=False)
    def _unlink_check(self):
        for property in self:
            if property.state not in ["new", "cancelled"]:
                raise UserError(
                    "You cannot delete a property that is not new or cancelled."
                )

    @api.depends("living_area", "garden_area", "garden")
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.living_area + (
                property.garden_area if property.garden else 0
            )

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for property in self:
            property.best_price = max(property.offer_ids.mapped("price"), default=0.0)

    @api.onchange("garden")
    def _onchange_garden(self):
        for property in self:
            if property.garden:
                property.garden_area = 10
                property.garden_orientation = "north"
            else:
                property.garden_area = 0
                property.garden_orientation = False

    def action_set_sold(self):
        for property in self:
            if property.selling_price > 0.0 and property.state != "cancelled":
                property.state = "sold"
            elif property.state == "cancelled":
                raise UserError("A cancelled property cannot be sold.")
            elif property.state == "new" or property.state == "offer received":
                raise UserError(
                    "This property must have an accepted offer before it can be sold."
                )
            elif property.state == "sold":
                raise UserError("This property is already sold.")

    def action_set_cancelled(self):
        for property in self:
            if property.state != "cancelled" and property.state != "sold":
                property.state = "cancelled"
            elif property.state == "cancelled":
                raise UserError("This property is already cancelled.")
            elif property.state == "sold":
                raise UserError("A sold property cannot be cancelled.")

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        for property in self:
            if float_is_zero(property.selling_price, precision_rounding=2):
                continue

            if (
                float_compare(
                    property.selling_price,
                    property.expected_price * 0.9,
                    precision_rounding=2,
                )
                < 0
            ):
                raise ValidationError(
                    "The selling price cannot be lower than 90'%' of the expected price!"
                )
