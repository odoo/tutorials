# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Contains all properties related to estate model"
    _order = "id desc"
    _inherit = ["mail.thread"]

    name = fields.Char(string="Title", required=True, tracking=True)
    sequence = fields.Char(string="Sequence", readonly=True, default="New")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(
        string="Available From", copy=False, default=lambda self: fields.Date.add(fields.Date.today(), months=3)
    )
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    description = fields.Text(string="Description")
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    facades = fields.Integer(string="Facades")
    living_area = fields.Integer(string="Living Area (sqm)")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West")
        ]
    )
    state = fields.Selection(
        string="Status",
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled")
        ],
        required=True,
        default="new",
        copy=False
    )
    active = fields.Boolean(default=True)
    total_area = fields.Integer(string="Total Area (sqm)", compute="_compute_total_area")
    best_price = fields.Float(string="Best Price", compute="_compute_best_price")
    company_id = fields.Many2one(string="Company", comodel_name="res.company", default=lambda self: self.env.company)
    tag_ids = fields.Many2many(string="Property Tags", comodel_name="estate.property.tag")
    property_type_id = fields.Many2one(string="Property Type", comodel_name="estate.property.type")
    offer_ids = fields.One2many(string="Offers", comodel_name="estate.property.offer", inverse_name="property_id")
    buyer_id = fields.Many2one(string="Buyer", comodel_name="res.partner", copy=False)
    salesperson_id = fields.Many2one(string="Salesperson", comodel_name="res.users", default=lambda self: self.env.user)

    _sql_constraints = [
        ("check_expected_price", "CHECK(expected_price > 0)", "Expected price must be strictly positive"),
        ("check_selling_price", "CHECK(selling_price >= 0)", "Selling price must be positive")
    ]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals["sequence"] = self.env["ir.sequence"].next_by_code("estate.property")
        return super().create(vals_list)

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        # selling_price should be atleast 90% of the expected_price, if offer is accepted
        for property in self:
            is_offer_accepted = any([offer.status == "accepted" for offer in property.offer_ids])
            if is_offer_accepted and float_compare(property.selling_price, 0.9 * property.expected_price, precision_digits=2) == -1:
                raise ValidationError("Selling price must be atleast 90% of the expected price")

    @api.ondelete(at_uninstall=False)
    def _unlink_property(self):
        for property in self:
            if property.state not in ["new", "cancelled"]:
                raise UserError("Only properties with a status of 'New' or 'Cancelled' can be deleted!")

    @api.depends("garden_area", "living_area")
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.garden_area + property.living_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for property in self:
            property.best_price = max([offer.price for offer in property.offer_ids], default=0)

    @api.onchange("garden")
    def _onchange_garden(self):
        for property in self:
            if property.garden:
                property.garden_area = 10
                property.garden_orientation = "north"
            else:
                property.garden_area = 0
                property.garden_orientation = None

    def action_sell_property(self):
        if self.state == "cancelled":
            raise UserError("Cancelled property cannot be sold")
        if not self.buyer_id.id:
            raise UserError("Property without buyer cannot be sold.")
        if not any([offer.status == "accepted" for offer in self.offer_ids]):
            raise UserError("You must accept an offer before selling the property.")
        self.state = "sold"

    def action_cancel_property(self):
        if self.state == "sold":
            raise UserError("Sold property cannot be cancelled")
        self.state = "cancelled"
