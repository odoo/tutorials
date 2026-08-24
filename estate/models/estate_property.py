from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _order = "id desc"

    name = fields.Char(required=True, string="Property Name", translate=True)
    description = fields.Text(translate=True)
    postcode = fields.Char()
    date_availability = fields.Date(
        default=lambda self: fields.Date.context_today(self) + relativedelta(months=3),
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    selling_date = fields.Date()
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[
            ('north', "North"),
            ('south', "South"),
            ('east', "East"),
            ('west', "West"),
        ],
        string="Garden Orientation",
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[
            ('new', "New"),
            ('offer_received', "Offer Received"),
            ('offer_accepted', "Offer Accepted"),
            ('booked', "Booked"),
            ('sold', "Sold"),
            ('cancelled', "Cancelled"),
        ],
        required=True,
        copy=False,
        default="new",
        string="State",
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson_id = fields.Many2one(
        "res.users",
        string="Salesperson",
        default=lambda self: self.env.user,
    )
    tag_ids = fields.Many2many("estate.property.tag", string="Property Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    maintenance_ids = fields.One2many(
        "estate.property.maintenance",
        "property_id",
        string="Maintenance Requests",
    )
    visit_ids = fields.One2many("estate.visit", "property_id", string="Visits")
    visit_count = fields.Integer(string="Visit Count", compute="_compute_visit_count")

    booking_ids = fields.One2many("estate.property.booking", "property_id", string="Bookings")
    booking_count = fields.Integer(string="Booking Count", compute="_compute_booking_count")

    total_area = fields.Integer(
        string="Total Area (sqm)",
        compute="_compute_total_area",
        help="Total area of the property (living area + garden area)",
    )
    best_price = fields.Float(
        string="Best Offer",
        compute="_compute_best_price",
        help="The highest offer received for this property",
        store=True,
    )
    square_area = fields.Integer(
        string="Square Area",
        compute="_compute_total_square",
    )

    _check_expected_price = models.Constraint(
        'CHECK(expected_price > 0)',
        'A property expected price must be positive',
    )
    _check_selling_price = models.Constraint(
        'CHECK(selling_price >= 0)',
        'A property selling price must be positive',
    )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("total_area")
    def _compute_total_square(self):
        for record in self:
            record.square_area = record.total_area * record.total_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            prices = record.offer_ids.mapped("price")
            if prices:
                record.best_price = max(prices)
            else:
                record.best_price = 0.0

    @api.depends("visit_ids")
    def _compute_visit_count(self):
        for record in self:
            record.visit_count = len(record.visit_ids)

    @api.depends("booking_ids")
    def _compute_booking_count(self):
        for record in self:
            record.booking_count = len(record.booking_ids)

    def action_view_visits(self):
        self.ensure_one()
        return {
            "name": "Visits",
            "type": "ir.actions.act_window",
            "res_model": "estate.visit",
            "view_mode": "list,form",
            "domain": [("property_id", "=", self.id)],
            "context": {"default_property_id": self.id},
        }

    def action_view_bookings(self):
        self.ensure_one()
        action = {
            "name": "Bookings",
            "type": "ir.actions.act_window",
            "res_model": "estate.property.booking",
            "domain": [("property_id", "=", self.id)],
            "context": {"default_property_id": self.id},
        }
        if len(self.booking_ids) == 1:
            action.update({
                "view_mode": "form",
                "res_id": self.booking_ids.id,
            })
        else:
            action.update({
                "view_mode": "list,form",
            })

        active_booking = self.booking_ids.filtered(lambda b: b.state in ("draft", "pending", "confirmed"))
        if active_booking or self.state != "offer_accepted":
            action["context"]["create"] = False

        return action

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_cancel(self):
        self.ensure_one()
        if self.state == "sold":
            msg = "A sold property cannot be cancelled."
            raise UserError(msg)
        active_booking = self.booking_ids.filtered(lambda b: b.state in ("draft", "pending", "confirmed"))
        if active_booking:
            active_booking.action_cancel_booking()
        self.write({"state": "cancelled", "active": False})
        return True

    def action_sold(self):
        self.ensure_one()
        if self.state == "cancelled":
            msg = "A cancelled property cannot be set as sold."
            raise UserError(msg)
        if not self.buyer_id:
            msg = "A property cannot be sold without an accepted offer (buyer)."
            raise UserError(msg)
        self.selling_date = fields.Date.today()
        create_date = self.create_date.date() if self.create_date else fields.Date.today()
        if (self.selling_date - create_date).days <= 2:
            tag = self.env['estate.property.tag'].search([('name', '=', 'quick sell')], limit=1)
            if not tag:
                tag = self.env['estate.property.tag'].create({
                    'name': 'quick sell',
                    'description': 'Quick sell property tag',
                })
            self.tag_ids = self.tag_ids | tag
        active_booking = self.booking_ids.filtered(lambda b: b.state in ("draft", "pending"))
        if active_booking:
            active_booking.write({"state": "confirmed"})
        self.write({"state": "sold", "active": False})
        return True

    def action_accept_best_offer(self):
        self.ensure_one()
        today = fields.Date.context_today(self)
        pending_offers = self.offer_ids.filtered(lambda o: not o.status)
        if not pending_offers:
            raise UserError(_("This property has no pending offers to accept."))
        valid_offers = pending_offers.filtered(lambda o: not o.date_deadline or o.date_deadline >= today)
        offers_to_select = valid_offers or pending_offers
        best_offer = max(offers_to_select, key=lambda o: (o.price, o.create_date or fields.Datetime.now(), o.id))
        best_offer.action_accept()
        return True

    @api.constrains('selling_price', 'expected_price')
    def _check_price_difference(self):
        for record in self:
            if not float_is_zero(record.selling_price, precision_rounding=0.01):
                if float_compare(record.selling_price, 0.9 * record.expected_price, precision_rounding=0.01) < 0:
                    msg = "The selling price cannot be lower than 90% of the expected price."
                    raise ValidationError(msg)
