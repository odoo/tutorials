from odoo import api, fields, models
from odoo.exceptions import ValidationError, UserError
from odoo.tools.float_utils import float_compare, float_is_zero
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate properties"
    _order = "id desc"

    active = fields.Boolean(string="Active", default=True)
    state = fields.Selection(
        [
            ("new", "New"),
            ("received", "Offer Received"),
            ("accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled")
        ],
        string="State",
        required=True,
        copy=False,
        default="new"
    )
    name = fields.Char(string="Name", required=True, default="Unknown")
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Availability", copy=False, default=fields.Date.today() + relativedelta(months=1))
    expected_price = fields.Float(string="Expected price", required=True)
    selling_price = fields.Float(string="Selling price", readonly=True, copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living area")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden area")
    garden_orientation = fields.Selection(
        [
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West")
        ],
        string="Garden facing",
        help="Garden facing"
    )
    last_seen = fields.Date(string="Last seen", default=fields.Datetime.now)
    property_type_id = fields.Many2one("estate.property.type", string="Type")
    buyer = fields.Many2one("res.partner", string="Buyer")
    salesperson = fields.Many2one("res.users", string="Salesperson", index=True, default=lambda self: self.env.user)
    tags_ids = fields.Many2many("estate.property.tags", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers", readonly=False)
    property_id = fields.Many2one("estate.property.type")
    validity = fields.Integer(string="Validity", default=7)
    total_area = fields.Integer(compute="_compute_total")
    best_offer = fields.Float(compute="_compute_maximum")
    date_deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_deadline", string="Deadline", default=fields.Date.today())

    @api.ondelete(at_uninstall=False)
    def _unlink_if_not_new_or_cancelled(self):
        for record in self:
            if not (record.state == 'new' or record.state == 'cancelled'):
                raise UserError("Cannot delete a record that is not new or canceled.")

    def action_estate_property_cancel(self):
        for record in self:
            if record.state != "sold":
                record.state = "cancelled"
            else:
                raise UserError("A sold property cannot be cancelled.")

    def action_estate_property_sold(self):
        for record in self:
            if record.state != "cancelled":
                if float_is_zero(record.selling_price, precision_rounding=0.01):
                    record.state = "received"
                    raise ValidationError("You cannot confirm a selling price of 0.")
                if float_compare(record.selling_price, record.expected_price * 0.9, precision_rounding=0.01) < 0:
                    record.state = "received"
                    raise ValidationError("The selling price cannot be lower than 90% of the expected price.")
                record.state = "sold"
            else:
                raise UserError("A cancelled property cannot be sold.")

    @api.depends("living_area", "garden_area")
    def _compute_total(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_maximum(self):
        for record in self:
            try:
                record.best_offer = max(offer.price for offer in record.offer_ids)
            except ValueError:
                record.best_offer = 0

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.to_date(record.create_date or fields.Date.today()) + relativedelta(days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            record.validity = (fields.Date.to_date(record.date_deadline) - fields.Date.to_date(record.create_date or fields.Date.today())).days

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = ""

    _sql_constrains = [
        ("check_prices", "CHECK(expected_price > 0 AND selling_price >= 0)", 
         "The expected price should be > 0 and the selling price should be >= 0.")
    ]
