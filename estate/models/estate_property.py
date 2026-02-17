from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools.date_utils import relativedelta
from odoo.tools.float_utils import float_compare

GARDEN_ORIENTATION = [("north", "North"), ("south", "South"), ("east", "East"), ("west", "West")]
PROPERTY_STATE = [("new", "New"), ("offer_received", "Offer Received"), ("offer_accepted", "Offer Accepted"), ("sold", "Sold"), ("cancelled", "Cancelled")]


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"

    name = fields.Char(string="Title", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Date Availability", copy=False, default=lambda self: fields.Date.context_today(self) + relativedelta(months=3))
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(string="Garden Orientation",
                                          selection=GARDEN_ORIENTATION)
    active = fields.Boolean(string="Active", default=True)
    state = fields.Selection(string="Status", selection=PROPERTY_STATE, required=True, copy=False, default="new")

    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer")
    salesman_id = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user)
    property_tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    total_area = fields.Integer(string="Total Area (sqm)", compute="_compute_total_area")
    best_offer = fields.Float(string="Best Offer", compute="_compute_best_offer")

    _check_expected_price = models.Constraint(
        'CHECK(expected_price > 0)',
        "The expected price must be strictly positive."
    )
    _check_selling_price = models.Constraint(
        'CHECK(selling_price >= 0)',
        "The selling price must be positive."
    )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.living_area + property.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for property in self:
            property.best_offer = max(property.offer_ids.mapped("price"), default=0)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_cancel_property(self):
        for property in self:
            if property.state == "sold":
                raise UserError("Sold properties cannot be cancelled")
            else:
                property.state = "cancelled"
        return True

    def action_sold_property(self):
        for property in self:
            if property.state == "cancelled":
                raise UserError("Cancelled properties cannot be sold")
            else:
                property.state = "sold"
        return True

    @api.constrains("selling_price")
    def _check_selling_price_minimum_ratio(self):
        for property in self:
            if not property.selling_price:
                continue
            if float_compare(property.selling_price, property.expected_price * 0.9, precision_digits=2) < 0:
                raise ValidationError("The selling price must be at least 90% of the expected price.")
