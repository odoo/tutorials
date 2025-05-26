import random
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "A real estate property"
    _order = "id desc"

    # TEXT FIELDS
    name = fields.Char(string="Property Name", required=True)
    description = fields.Text(string="Estate Description")
    postcode = fields.Char()

    # NUMBER & BOOL FIELDS
    active = fields.Boolean(default=True)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=random.randint(2, 6))
    facades = fields.Integer()
    living_area = fields.Integer()
    garden_area = fields.Integer()

    garage = fields.Boolean()
    garden = fields.Boolean()

    # DATE FIELDS
    date_availability = fields.Date(
        string="Available From",
        copy=False,
        default=lambda self: self._three_months_from_now()
    )

    # STATE FIELDS
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        default="new",
        string="State",
        required=True,
        copy=False,
    )

    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"),
            ("east", "East"),
            ("south", "South"),
            ("west", "West"),
        ],
    )

    # RELATED FIELDS
    property_type_id = fields.Many2one("estate.property.type", string="Type")
    property_tag_ids = fields.Many2many("estate.property.tag", string="Tag")

    property_offer_ids = fields.One2many(
        comodel_name="estate.property.offer",
        inverse_name="property_id",
        string="Offers",
    )
    partner_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    user_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)

    # COMPUTED FIELDS
    total_area = fields.Integer(compute="_compute_total_area")
    best_offer = fields.Float(compute="_compute_best_offer")

    # -----------  BUSINESS LOGIC  -------------- #

    @api.depends("property_offer_ids.price")
    def _compute_best_offer(self):
        for record in self:
            record.best_offer = max(record.property_offer_ids.mapped("price"), default=0)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.model
    def _three_months_from_now(self):
        """Return an ORM-compliant date three months from today."""
        return fields.Date.today() + relativedelta(months=3)

    # -----------  MODEL ACTIONS  -------------- #

    def action_cancel_listing(self):
        for record in self:
            if record.state == "sold":
                raise UserError("This listing is already sold and can't be cancelled")
            record.state = "cancelled"
        return True

    def action_sell_listing(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError("This listing is already cancelled and can't be sold")
            record.state = "sold"
        return True

    # -----------  MODEL CONSTRAINTS  -------------- #

    @api.ondelete(at_uninstall=False)
    def _unlink_if_state_valid(self):
        if any(property.state not in ["new", "cancelled"] for property in self):
            raise UserError("Can't delete an active property listing!")

    # Constraining on state instead of selling price because selling price is not a writable field
    @api.constrains("selling_price", "expected_price")
    def _onchange_price(self):
        if not float_is_zero(self.selling_price, 10) and self.selling_price < 0.9 * self.expected_price:
            raise ValidationError("Selling price can't be lower then 0.9 * expected price !")

    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', 'Property name should be unique'),
        ('positive_expected_price', 'CHECK(expected_price >= 0)', 'Expected price should be > 0'),
    ]

    # ------------- HELPERS --------------- #

    def set_offer_received(self):
        if self.state == "new":
            self.write({"state": "offer_received"})
