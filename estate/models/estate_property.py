from odoo import api, exceptions, fields, models
from datetime import date, timedelta
from odoo.exceptions import ValidationError, UserError
from odoo.tools.float_utils import float_compare, float_is_zero


class estate(models.Model):
    _name = "estate.property"
    _description = "Estate Property Plans"
    _order = "id desc"

    name = fields.Char(required=True)
    description = fields.Text("Description")
    postcode = fields.Char("Postcode")
    date_availability = fields.Date("Date Availibility", default=lambda self: date.today() + timedelta(days=90), copy=False)
    expected_price = fields.Float("Expected Price", required=True)
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
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string="Status",
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        required=True, copy=False, default="new",
    )
    property_type_id = fields.Many2one(comodel_name="estate.property.type", string="Property Type")
    salesperson_id = fields.Many2one("res.users", string="Sales Person", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    tag_ids = fields.Many2many(comodel_name="estate.property.tags", string="Property Tag")
    offer_ids = fields.One2many(comodel_name="estate.property.offer", inverse_name="property_id", string="Property Offer")
    total_area = fields.Integer(compute="_compute_totalarea")
    best_price = fields.Integer("Best Offer", compute="_compute_best_price")
    can_be_sold = fields.Boolean("Can be Sold", compute="_compute_can_be_sold")
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    image = fields.Binary("Image", attachment=True)

    @api.depends("state")
    def _compute_can_be_sold(self):
        for record in self:
            record.can_be_sold = (self.env["ir.config_parameter"].sudo().get_param("estate.property_sold") == "True")

    @api.depends("living_area", "garden_area")
    def _compute_totalarea(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                if record.state == "new":
                    record.state = "offer_received"
                record.best_price = max(record.offer_ids.mapped("price"))
            else:
                record.best_price = 0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = ""

    def action_cancel(self):
        for record in self:
            if record.state == "sold":
                raise exceptions.UserError("Cannot cancel a property that is already sold!")
            record.state = "cancelled"

    def action_sold(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError("Cannot sell a property that is already cancelled!")
                return False
            elif not record.buyer_id:
                raise UserError("The property must have a buyer before creating an invoice.")
                return False
            else:
                record.state = "sold"
                return True

    _sql_constraints = [
        ("check_expected_price", "CHECK(expected_price > 0)", "Expected Price must be strictly positive"),
        ("check_selling_price", "CHECK(selling_price >= 0)", "Selling Price must be positive"),
    ]

    @api.constrains("selling_price", "expected_price")
    def _check_price(self):
        if float_compare(self.selling_price, 0.9 * self.expected_price, 2) == -1 and not float_is_zero(self.selling_price, 2):
            raise ValidationError("selling price must greater than 90% of expected price")

    @api.ondelete(at_uninstall=False)
    def _unlink_estateproperty(self):
        for record in self:
            if record.state not in ["new", "cancelled"]:
                raise UserError("Can't delete property!")
