from odoo import api, fields, models
from odoo.tools import relativedelta
from odoo.exceptions import UserError, ValidationError
from odoo.tools.translate import _
from odoo.tools.float_utils import float_compare, float_is_zero

from .. import util


class EstateModel(models.Model):
    _name = "estate.property"
    _description = "Get rich fast"
    _order = "id desc"

    def _get_default_date_availability(self):
        today = fields.Date.today()
        return today + relativedelta(months=3)

    def _get_default_salesperson_id(self):
        employee_rec = self.env["hr.employee"].search([("user_id", "=", self.env.uid)], limit=1)
        return employee_rec.id

    name = fields.Char("Name", required=True)
    property_type_id = fields.Many2one("estate.property.type", string="Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson_id = fields.Many2one("hr.employee", string="Salesperson", default=_get_default_salesperson_id)
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    best_price = fields.Float("Best Price", compute="_compute_best_price")
    property_tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    description = fields.Text("Description")
    postcode = fields.Char("Postcode")
    date_availability = fields.Date("Available From", copy=False, default=_get_default_date_availability)
    expected_price = fields.Float("Expected Price", required=True, default=1e6)
    selling_price = fields.Float("Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer("Bedrooms", default=2)
    living_area = fields.Integer("Living Area (sqm)")
    total_area = fields.Integer("Total Area (sqm)", compute="_compute_total_area")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden Area (sqm)")
    garden_orientation = fields.Selection(string="Garden Orientation", selection=[
        ("north", "North"),
        ("south", "South"),
        ("east", "East"),
        ("west", "West"),
    ])

    state = fields.Selection(string="State", required=True, default="new", selection=[
        ("new", "New"),
        ("offer_received", "Offer Received"),
        ("offer_accepted", "Offer Accepted"),
        ("sold", "Sold"),
        ("canceled", "Canceled"),
    ])

    active = fields.Boolean("Active", default=True)

    _sql_constraints = [
        ("check_expected_price", "check(expected_price > 0)", "Expected price must be strictly positive"),
        ("check_selling_price", "check(selling_price >= 0)", "Selling price must be positive"),
    ]

    def register_accepted_offer(self, buyer_id, selling_price):
        self.write({
            "buyer_id": buyer_id,
            "selling_price": selling_price,
        })

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.write({"total_area": record.living_area + record.garden_area})

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.write({"best_price": max(record.offer_ids.mapped("price"), default=0.)})

    @api.onchange("garden")
    def _onchange_garden(self):
        self.ensure_one()

        if self.garden:
            area = self.garden_area or 10
            orient = self.garden_orientation or "north"
        else:
            area = 0
            orient = False

        self.write({
            "garden_area": area,
            "garden_orientation": orient,
        })

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        for record in self:
            if float_is_zero(record.selling_price, precision_digits=2):
                continue
            if float_compare(record.expected_price * .9, record.selling_price, precision_digits=2) == 1:
                raise ValidationError(_("Selling price cannot be lower than 90% of the expected price"))

    @api.ondelete(at_uninstall=False)
    def _must_be_new_or_cancelled(self):
        VALID_STATES_TO_DELETE = ["new", "canceled"]
        for record in self:
            if record.state not in VALID_STATES_TO_DELETE:
                raise UserError(_("A property can only be deleted if new or canceled"))

    @util.action
    def action_set_sold(self):
        self.ensure_one()
        if self.state == "canceled":
            raise UserError(_("A property can't be sold after it was canceled"))
        self.write({"state": "sold"})

    @util.action
    def action_set_canceled(self):
        self.ensure_one()
        if self.state == "sold":
            raise UserError(_("A property can't be canceled after it was sold"))
        self.write({"state": "canceled"})
