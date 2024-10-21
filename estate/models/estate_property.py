from odoo import api, fields, models
from odoo.exceptions import ValidationError, UserError
from odoo.tools.float_utils import float_is_zero
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real estate property"
    _order = "id desc"

    name = fields.Char(string="Title", required=True, translate=True)
    description = fields.Text(string="Description", translate=True)
    image = fields.Image("Image")
    tags = fields.Many2many("estate.property.tag", string="Tags")
    salesman_id = fields.Many2one(
        "res.partner", string="Salesman", default=lambda self: self.env.user
    )
    buyer_id = fields.Many2one("res.users", string="Buyer", copy=False)
    postcode = fields.Char(string="Postcode", required=True)
    property_type_id = fields.Many2one(
        "estate.property.type", string="Property Type", required=True
    )
    date_availability = fields.Date(
        string="Available From",
        default=fields.Date.today() + relativedelta(months=3),
        copy=False,
    )
    expected_price = fields.Float(string="Expected Price", required=True)
    best_offer = fields.Float(
        string="Best Offer", compute="_compute_best_offer", store=True
    )
    offers_id = fields.Many2many("estate.property.offer", string="Offers", copy=False)
    selling_price = fields.Float(string="Selling Price", readonly=True)
    active = fields.Boolean(string="Active", default=True)
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
            ("west", "West"),
            ("south", "South"),
            ("east", "East"),
        ],
    )
    total_area = fields.Float(string="Total Area (sqm)", compute="_compute_total_area")
    state = fields.Selection(
        string="Status",
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        required=True,
        copy=False,
        default="new",
    )

    _sql_constraints = [
        (
            "check_bedrooms",
            "CHECK(bedrooms >= 0)",
            "Can't have a negative number of bedrooms.",
        ),
        (
            "check_areas",
            "CHECK(garden_area >= 0 AND living_area >= 0)",
            "Can't have a negative size surfaces.",
        ),
        (
            "check_positive_price",
            "CHECK(expected_price >= 0 AND selling_price >= 0)",
            "Expected price and selling price must be positive.",
        ),
        (
            "check_selling_price",
            "CHECK(selling_price = 0 OR selling_price >= 0.9 * expected_price)",
            "Selling price must be at least 90% of expected price.",
        ),
    ]

    @api.depends("living_area", "garden_area", "garden")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + (
                record.garden_area if record.garden else 0
            )

    @api.depends("offers_id")
    def _compute_best_offer(self):
        for record in self:
            record.best_offer = (
                max(record.offers_id.mapped("price"))
                if len(record.offers_id) > 0
                else 0
            )

    @api.onchange("garden")
    def _onchange_garden(self):
        self.garden_area = 10
        self.garden_orientation = "north"

    @api.onchange("offers_id")
    def _onchange_offers(self):
        if len(self.offers_id) > 0 and "new":
            self.state = "offer_received"
        elif len(self.offers_id) == 0:
            self.state = "new"
            self.buyer_id = None
            self._compute_best_offer()
            self.selling_price = 0

    def action_state(self):
        action = self.env.context.get("action")
        self.active = False
        match action:
            case "sell":
                if self.state != "cancelled" and self.selling_price > 0:
                    self.state = "sold"
                elif float_is_zero(self.selling_price):
                    raise ValidationError(
                        "Selling price could not be found."
                    )
                else:
                    raise UserError(
                        "Can't sell a cancelled property. Try resetting to draft."
                    )
            case "cancel":
                if self.state != "sold":
                    self.state = "cancelled"
                else:
                    raise UserError(
                        "Can't cancel a sold property. Try resetting to draft."
                    )
            case _:
                self.state = "new"
                self.buyer_id = None
                self._compute_best_offer()
                self.selling_price = 0
                for offer in self.offers_id:
                    offer.status = "pending"
                self.active = True
        return True
