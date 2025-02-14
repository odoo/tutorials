from odoo import api, fields, models
from odoo.tools import float_is_zero, float_compare
from odoo.exceptions import UserError, ValidationError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _order = "id desc"
    _inherit="mail.thread"

    name = fields.Char("Name", required=True)
    description = fields.Text("Description")
    postcode = fields.Char("Postcode")
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    date_availability = fields.Date(
        "Available From",
        default=fields.Date.add(fields.Date.today(), months=3),
        copy=False,
    )
    expected_price = fields.Float("Expected Price", required=True, tracking=True)
    selling_price = fields.Float("Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer("Bedrooms", default=2)
    living_area = fields.Integer("Living Area")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden Area")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
    )
    active = fields.Boolean(
        "Active",
        default=True,
        tracking=True,
        help="Mark as active if you want the property to be listed.",
    )
    state = fields.Selection(
        string="State",
        required=True,
        readonly=True,
        default="new",
        copy=False,
        selection=[
            ("new", "New"),
            ("offer received", "Offer Received"),
            ("offer accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled"),
        ],
        tracking=True,
    )

    salesman_id = fields.Many2one(
        "res.users", string="Salesman", default=lambda self: self.env.user
    )
    buyer_id = fields.Many2one("res.partner", copy=False, string="Buyer", tracking=True)

    tag_ids = fields.Many2many("estate.property.tag", string="Tags", tracking=True)

    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    total_area = fields.Integer("Total Area", compute="_compute_total_area")
    best_price = fields.Float("Best Price", compute="_compute_best_price")
    company_id = fields.Many2one("res.company", default=lambda self: self.env.company, required=True)

    _sql_constraints = [
        (
            "check_expected_price",
            "CHECK(expected_price > 0)",
            "The expected price must be strictly positive.",
        ),
    ]

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
            self.garden_orientation = ""

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        for record in self:
            if float_is_zero(record.selling_price, precision_rounding=self.env.company.currency_id.rounding):
                continue
            if float_compare(record.selling_price, record.expected_price * 0.9, precision_rounding=self.env.company.currency_id.rounding)< 0:
                raise ValidationError("The selling price cannot be lower than 90% of the expected price!")

    @api.ondelete(at_uninstall=False)
    def _unlink_property(self):
        for record in self:
            if record.state not in ["new", "canceled"]:
                raise UserError("You can only delete properties in 'New' or 'Canceled' state.")


    def action_set_sold(self):
        for record in self:
            if record.state != "canceled":
                record.state = "sold"
            elif record.state == "canceled":
                raise UserError("Canceled properties cannot be sold")
            elif record.state == "sold":
                raise UserError("It's already been sold.")
            return True

    def action_set_cancel(self):
        for record in self:
            if record.state != "sold":
                record.state = "canceled"
            elif record.state == "sold":
                raise UserError("Sold properties cannot be canceled.")
            elif record.state == "canceled":
                raise UserError("It's already been canceled.")
            return True
