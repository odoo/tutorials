from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _sql_constraints = [
        (
            "estate_property_expected_price_positive",
            "CHECK(expected_price > 0)",
            "The expected price must be positive.",
        ),
        (
            "estate_property_selling_price_non_negative",
            "CHECK(selling_price >= 0)",
            "The selling price must be non negative.",
        ),
    ]

    _order = "id desc"

    name = fields.Char(string="Property Name", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(
        string="Available From",
        copy=False,
        default=fields.Date.today() + relativedelta(months=4),
    )
    expected_price = fields.Float(string="Expected Price")
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
        string="Garden Orientation",
    )
    active = fields.Boolean(string="Active", default=True)
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        string="Status",
        required=True,
        copy=False,
        default="new",
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson_id = fields.Many2one(
        "res.users", string="Salesperson", default=lambda self: self.env.user
    )
    tag_ids = fields.Many2many(
        "estate.property.tags", string="Tags", help="Tags for the property"
    )
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Integer(
        string="Total Area (sqm)",
        compute="_compute_total_area",
        store=True,
    )
    company_id = fields.Many2one(
        "res.company", required=True, default=lambda self: self.env.company
    )
    best_price = fields.Float(
        string="Best Price",
        compute="_compute_best_price",
        store=True,
    )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped("price"))
            else:
                record.best_price = 0.0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = ""

    def action_set_sold(self):
        for offer in self:
            if offer.state == "sold":
                raise UserError("This property is already sold.")
            if offer.state == "offer_accepted":
                offer.state = "sold"
                return True
            else:
                raise UserError("Only accepted offers can set the property as sold.")

    def action_set_cancel(self):
        for offer in self:
            if offer.state == "new":
                offer.state = "cancelled"
                return True
            else:
                raise UserError(
                    "Only refused offers can set the property as cancelled."
                )

    @api.constrains("selling_price", "expected_price")
    def _check_price(self):
        for record in self:
            if record.selling_price and record.expected_price:
                if record.selling_price < 0.9 * record.expected_price:
                    raise ValidationError(
                        "The selling price must be at least 90% of the expected price."
                    )

    @api.ondelete(at_uninstall=False)
    def _ondelete_property(self):
        for record in self:
            if record.state not in ["new", "cancelled"]:
                raise UserError(
                    "You cannot delete a property that is not new or cancelled."
                )

    @api.onchange("offer_ids")
    def _onchange_offer_ids(self):
        if not self.offer_ids and self.state != "new":
            self.state = "new"

    @api.onchange("state")
    def _onchange_state(self):
        if self.state == "offer_received" and not self.offer_ids:
            raise UserError("No offers available yet!.")
        elif self.state == "offer_received" and self.offer_ids.filtered(
            lambda o: o.status == "accepted"
        ):
            raise UserError(
                "You cannot set the property as offer received when there is an accepted offer."
            )
        elif self.state == "offer_accepted" and not self.offer_ids:
            raise UserError("You cannot accept an offer without any offers.")
        elif self.state == "sold" and not self.offer_ids:
            raise UserError("You cannot sell a property without any offers.")
        elif self.state == "offer_accepted" and not self.offer_ids.filtered(
            lambda o: o.status == "accepted"
        ):
            raise UserError(
                "You cannot set the property as offer accepted without an accepted offer."
            )
