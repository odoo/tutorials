from odoo import api, fields, models  # type: ignore
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero
from datetime import timedelta


class EstateProterty(models.Model):
    _name = "estate_property"
    _description = "estate property"

    name = fields.Char(string="Title", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(
        string="Available From",
        default=fields.Date.today() + timedelta(days=90),
        copy=False,
    )
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", copy=False, readonly=True)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden", store=True)
    garden_area = fields.Integer(string="Garden area (sqm)")
    garden_orientation = fields.Selection(
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
        string="Garden Orientation",
    )

    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer received", "Offer Received"),
            ("offer accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled"),
        ],
        string="State",
        default="new",
        copy=False,
        required=True,
    )
    estate_property_type_id = fields.Many2one("estate_property_type", string="Type")
    user_id = fields.Many2one(
        "res.users",
        string="Salesperson",
        index=True,
        default=lambda self: self.env.user,
    )
    buyer = fields.Char(string="buyer", copy=False)
    tag_ids = fields.Many2many("estate_property_tag", string="Tags")
    offer_ids = fields.One2many("estate_property_offer", "property_id", string="Offer")
    total_area = fields.Float(compute="_compute_total_area")
    best_price = fields.Float(string="Best offer", compute="_compute_best_price")

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"), default=0.0)

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_sold(self):
        if self.state == "canceled":
            raise UserError("A canceled property cannot be sold")
        else:
            self.state = "sold"
        return True

    def action_cancel(self):
        if self.state == "sold":
            raise UserError("sold property cannot be canceled")
        else:
            self.state = "canceled"
        return True

    @api.constrains("expected_price", "selling_price")
    def _check_positif(self):
        for record in self:
            if record.expected_price <= 0:
                raise ValidationError("Expected price must be positif")
            if record.selling_price < 0:
                raise ValidationError("Selling price must be positif")

    @api.constrains("expected_price", "selling_price")
    def _check_selling_price(self):
        for record in self:
            if not float_is_zero(record.selling_price, precision_digits=2) and not float_is_zero(record.expected_price, precision_digits=2):
                if float_compare(record.selling_price, 0.9 * record.expected_price, precision_digits=2) < 0:
                    raise models.ValidationError("Selling price cannot be lower than 90% of the expected price.")
