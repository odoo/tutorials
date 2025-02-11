from odoo import api, fields, models
from datetime import timedelta
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    name = fields.Char(
        string="Name", required=True, help="Name of the Property"
    )
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(
        string="Available From",
        copy=False,
        default=lambda self: fields.Datetime.today() + timedelta(days=90),
    )
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area(sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area(sqm)")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
    )
    active = fields.Boolean(string="Active", default=True)
    status = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        default="new",
        copy=False,
        readonly=True
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False, readonly=True)
    salesperson_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag", string="Property Tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Property Offer")

    total_area = fields.Float(compute="_compute_total_area", string="Total Area(sqm)")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
    best_price = fields.Float(compute="_compute_best_price")

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
            self.garden_orientation = False

    def action_property_sold(self):
        for record in self:
            if record.status == "cancelled":
                raise exceptions.UserError("A cancelled property cannot be sold!")

            accepted_offer = record.offer_ids.filtered(lambda o: o.status == 'accepted')
            if not accepted_offer:
                raise exceptions.UserError("You need to accept an offer first!")

            record.status = 'sold'
        return True

    def action_property_cancel(self):
        for record in self:
            if record.status == 'sold':
                raise exceptions.UserError("A sold property cannot be cancelled!")
            record.status = 'cancelled'
        return True

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 'The expected price must be positive.'),
        ('check_selling_price', 'CHECK(selling_price >= 0)', 'The selling price must be positive.')
    ]

    @api.constrains("expected_price", "selling_price")
    def _check_selling_price(self):
        for record in self:
            if float_is_zero(record.selling_price, precision_digits=2):
                continue
            min_acceptable_price = record.expected_price * 0.9
            if float_compare(record.selling_price, min_acceptable_price, precision_digits=2) == -1:
                raise ValidationError("The selling price cannot be lower than 90% of the expected price!")
