from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare


class Property(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _order = "id desc"

    name = fields.Char("Property Name", required=True)
    description = fields.Text("Property Description")
    postcode = fields.Char("Postcode")

    date_availability = fields.Date("Available Date", copy=False, default=lambda _x: datetime.now() + relativedelta(months=+3))

    expected_price = fields.Float("Expected Price")
    selling_price = fields.Float("Selling Price", copy=False, readonly=True)
    best_price = fields.Float("Best offer", compute="_compute_best_price")

    bedrooms = fields.Integer("Number of Bedrooms", default=2)
    living_area = fields.Integer("Living Area")
    facades = fields.Integer("Number of Facades")

    has_garage = fields.Boolean("Has a Garage")
    has_garden = fields.Boolean("Has a Garden")
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

    state = fields.Selection(
        string="Property State",
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        default="new",
    )

    total_area = fields.Integer("Total Area", compute="_compute_total_area")

    property_type_id = fields.Many2one("estate.property.type", string="Property Type")

    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    seller_id = fields.Many2one("res.users", string="Seller", default=lambda self: self.env.user)

    tags_ids = fields.Many2many("estate.property.tag", string="Property Tags")

    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    active = fields.Boolean(default=True)

    _check_expected_price = models.Constraint("CHECK(expected_price > 0)", "Expected price must be greater than zero")
    _check_selling_price = models.Constraint("CHECK(selling_price >= 0)", "Selling price must be greater or equal to zero")

    @api.constrains("expected_price", "selling_price")
    def _check_selling_price_proportion(self):
        for record in self:
            if record.selling_price == 0:
                continue  # 0 means no offer accepted

            if float_compare(record.selling_price, 0.9 * record.expected_price, 2) < 0:
                raise ValidationError(_("Selling price must be at least 90 percent of expected price"))

    def action_mark_as_sold(self):

        if "cancelled" in self.mapped("state"):
            raise UserError(_("Can't sell a cancelled auction."))

        for record in self:
            record.state = "sold"

        return True

    def action_cancel_selling(self):

        if "sold" in self.mapped("state"):
            raise UserError(_("Can't cancel a sold auction."))

        for record in self:
            record.state = "cancelled"

        return True

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"), default=0.0)

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.onchange("has_garden")
    def _onchange_has_garden(self):
        if self.has_garden:
            self.garden_area = 10
            self.garden_orientation = "north"
            return

        self.garden_area = 0
        self.garden_orientation = False
