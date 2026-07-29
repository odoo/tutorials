from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class AwesomeEstateProperty(models.Model):
    _name = 'awesome.estate.property'
    _description = 'Real Estate Property'
    _rec_name = 'name'
    _order = 'id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _mail_post_access = 'read'

    # -----------------------------------------------------------------------
    # Fields
    # -----------------------------------------------------------------------
    name = fields.Char(string="Title", required=True, tracking=1)
    image_1920 = fields.Image(
        "Property Image",
        max_width=1920,
        max_height=1920,
        help="Upload a photo of the property. Images are automatically resized to 1920px.",
    )
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        string="Available From",
        copy=False,
        default=lambda self: fields.Date.add(fields.Date.context_today(self), months=3),
        tracking=1,
    )
    expected_price = fields.Float(required=True, tracking=10)
    selling_price = fields.Float(copy=False, tracking=20)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        [
            ('north', "North"),
            ('south', "South"),
            ('east', "East"),
            ('west', "West"),
        ],
    )
    property_type_id = fields.Many2one(
        'awesome.estate.property.type',
        string="Property Type",
        ondelete='set null',
        index=True,
    )
    buyer_id = fields.Many2one(
        'res.partner',
        string="Buyer",
        readonly=True,
        copy=False,
        ondelete='set null',
        index=True,
        tracking=1,
    )
    salesperson_id = fields.Many2one(
        'res.users',
        string="Salesperson",
        default=lambda self: self.env.user,
        ondelete='set null',
        index=True,
        tracking=1,
    )
    tag_ids = fields.Many2many(
        'awesome.estate.property.tag',
    )
    offer_ids = fields.One2many(
        'awesome.estate.property.offer',
        'property_id',
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        [
            ('new', "New"),
            ('offer_received', "Offer Received"),
            ('offer_accepted', "Offer Accepted"),
            ('sold', "Sold"),
            ('canceled', "Canceled"),
        ],
        string="Status",
        required=True,
        copy=False,
        default='new',
        tracking=50,
    )
    total_area = fields.Integer(
        string="Total Area (sqm)",
        compute='_compute_total_area',
        store=True,
        help="Total area computed by summing the living area and the garden area.",
    )
    best_price = fields.Float(
        string="Best Offer",
        compute='_compute_best_price',
        store=True,
        help="Best offer received.",
    )
    maintenance_ids = fields.One2many(
        'awesome.estate.property.maintenance',
        'property_id',
        string="Maintenance Requests",
    )
    suspicious_offer_count = fields.Integer(
        string="Suspicious Offers",
        compute='_compute_suspicious_offer_count',
        help="Number of offers marked as suspicious on this property.",
    )

    visit_ids = fields.One2many(
        'awesome.estate.property.visit', 'property_id', string="Visits"
    )
    visit_count = fields.Integer(string="Visit Count", compute='_compute_visit_count')

    # -----------------------------------------------------------------------
    # SQL Constraints
    # -----------------------------------------------------------------------
    _check_living_area = models.Constraint(
        'CHECK (living_area >= 0 AND living_area <= 100000)',
        "Living area must be between 0 and 100,000 sqm. Please enter a realistic value.",
    )
    _check_garden_area = models.Constraint(
        'CHECK (garden_area >= 0 AND garden_area <= 100000)',
        "Garden area must be between 0 and 100,000 sqm. Please enter a realistic value.",
    )
    _check_expected_price = models.Constraint(
        'CHECK (expected_price > 0)',
        "Expected price must be greater than zero.",
    )
    _check_selling_price_positive = models.Constraint(
        'CHECK (selling_price >= 0)',
        "The selling price must be positive.",
    )
    _check_bedrooms = models.Constraint(
        'CHECK (bedrooms >= 0)',
        "Bedrooms cannot be negative.",
    )
    _check_facades = models.Constraint(
        'CHECK (facades >= 0)',
        "Facades cannot be negative.",
    )

    # -----------------------------------------------------------------------
    # Python Constraints
    # -----------------------------------------------------------------------
    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        """Only validate selling price floor when set manually, not via offer accept."""
        if self.env.context.get('accepting_offer'):
            return
        for record in self:
            if (
                float_is_zero(record.selling_price, precision_digits=2)
                or not record.expected_price
            ):
                continue
            if (
                float_compare(
                    record.selling_price,
                    record.expected_price * 0.9,
                    precision_digits=2,
                )
                == -1
            ):
                raise ValidationError(
                    _(
                        "The selling price cannot be lower than 90%% of the expected price."
                    ),
                )

    # -----------------------------------------------------------------------
    # Compute Methods
    # -----------------------------------------------------------------------
    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids', 'offer_ids.price', 'offer_ids.status')
    def _compute_best_price(self):
        """Best price among pending (non-refused, non-accepted) offers only."""
        for record in self:
            pending = record.offer_ids.filtered(lambda o: not o.status)
            prices = pending.mapped('price')
            record.best_price = max(prices) if prices else 0.0

    @api.depends('offer_ids.is_suspicious')
    def _compute_suspicious_offer_count(self):
        for record in self:
            record.suspicious_offer_count = len(
                record.offer_ids.filtered('is_suspicious')
            )

    @api.depends('visit_ids')
    def _compute_visit_count(self):
        for prop in self:
            prop.visit_count = len(prop.visit_ids)

    def action_view_visits(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _("Visits"),
            'res_model': 'awesome.estate.property.visit',
            'view_mode': 'calendar,list,form',
            'domain': [('property_id', '=', self.id)],
            'context': {
                'default_property_id': self.id,
                'default_agent_id': self.salesperson_id.id if self.salesperson_id else self.env.user.id,
            },
        }

    # -----------------------------------------------------------------------
    # Onchange Methods
    # -----------------------------------------------------------------------
    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    # -----------------------------------------------------------------------
    # CRUD Methods
    # -----------------------------------------------------------------------
    @api.ondelete(at_uninstall=False)
    def _unlink_if_not_canceled(self):
        if any(record.state not in ('new', 'canceled') for record in self):
            raise UserError(
                _("You cannot delete a property with an active or sold status.")
            )

    # -----------------------------------------------------------------------
    # Action Methods
    # -----------------------------------------------------------------------
    def action_sold(self):
        """Mark the property as sold."""
        self.ensure_one()
        if self.state == 'canceled':
            raise UserError(_("Canceled properties cannot be sold."))
        if self.state == 'sold':
            raise UserError(_("Property is already sold."))
        open_maint = self.maintenance_ids.filtered(
            lambda m: m.state not in ('done', 'canceled')
        )
        if open_maint:
            raise UserError(
                _(
                    "Cannot sell a property with open maintenance requests. "
                    "Complete or cancel them first."
                )
            )
        if self.state == 'offer_accepted' and not self.selling_price:
            accepted = self.offer_ids.filtered(lambda o: o.status == 'accepted')
            if accepted:
                self.write(
                    {
                        'selling_price': accepted.price,
                        'buyer_id': accepted.partner_id.id,
                    }
                )
        if not self.selling_price:
            raise UserError(_("Set a selling price before selling the property."))
        self.state = 'sold'
        return True

    def action_cancel(self):
        """Cancel the property and refuse all pending offers."""
        self.ensure_one()
        if self.state == 'sold':
            raise UserError(_("Sold properties cannot be canceled."))
        if self.state == 'canceled':
            raise UserError(_("Property is already canceled."))
        open_maint = self.maintenance_ids.filtered(
            lambda m: m.state not in ('done', 'canceled')
        )
        if open_maint:
            raise UserError(
                _(
                    "Cannot cancel a property with open maintenance requests. "
                    "Complete or cancel them first."
                )
            )
        pending = self.offer_ids.filtered(lambda o: not o.status)
        if pending:
            pending.status = 'refused'
        accepted = self.offer_ids.filtered(lambda o: o.status == 'accepted')
        if accepted:
            self.message_post(
                body=_(
                    "Property '%s' was cancelled. The accepted offer "
                    "from %s for %.2f is no longer valid.",
                    self.display_name,
                    accepted.partner_id.display_name,
                    accepted.price,
                )
            )
        self.state = 'canceled'
        self.active = False
        return True

    def action_reset(self):
        """Reset sold or canceled property back to 'new' and reopen all offers."""
        self.ensure_one()
        if self.state not in ('sold', 'canceled'):
            raise UserError(_("Only sold or canceled properties can be reset."))
        self.write(
            {
                'state': 'new',
                'selling_price': 0.0,
                'buyer_id': False,
                'active': True,
            }
        )
        self.offer_ids.write({'status': False})
        return True

    def action_accept_best_offer(self):
        """Accept the highest-priced pending offer in one click."""
        self.ensure_one()
        if self.state in ('sold', 'canceled', 'offer_accepted'):
            raise UserError(
                _("Cannot accept offers on a property that is %s.", self.state),
            )
        best_offers = self.offer_ids.filtered(lambda o: o.price == self.best_price)
        if not best_offers:
            raise UserError(_("No offers available to accept."))
        best_offers[0].action_accept()

    # -----------------------------------------------------------------------
    # Cron Methods
    # -----------------------------------------------------------------------
    @api.model
    def _cron_archive_stale_properties(self):
        """Weekly cron: auto-cancel properties with no activity for 90+ days."""
        limit_date = fields.Date.add(fields.Date.today(), days=-90)
        stale_new = self.search(
            [
                ('state', '=', 'new'),
                ('offer_ids', '=', False),
                ('create_date', '<', fields.Datetime.to_datetime(limit_date)),
            ]
        )
        for record in stale_new:
            record.message_post(
                body=_(
                    "This property has been automatically archived because it "
                    "received no offers for 90 days."
                )
            )
            record.write({'active': False, 'state': 'canceled'})
        stale_received = self.search(
            [
                ('state', '=', 'offer_received'),
                ('create_date', '<', fields.Datetime.to_datetime(limit_date)),
            ]
        )
        for record in stale_received:
            pending = record.offer_ids.filtered(lambda o: not o.status)
            if not pending:
                record.message_post(
                    body=_(
                        "This property has been automatically archived because "
                        "all its offers are final and none are pending."
                    )
                )
                record.write({'active': False, 'state': 'canceled'})
        return True

    @api.model
    def _cron_remind_expiring_offers(self):
        """Daily cron: notify salesperson 1 day before an offer's deadline expires."""
        tomorrow = fields.Date.add(fields.Date.today(), days=1)
        near_expiry = self.env['awesome.estate.property.offer'].search(
            [
                ('date_deadline', '=', tomorrow),
                ('status', 'not in', ['accepted', 'refused']),
            ]
        )
        for offer in near_expiry:
            offer.property_id.activity_schedule(
                'mail.mail_activity_data_todo',
                summary=_(
                    "Offer deadline expires tomorrow — %(price).0f from %(partner)s",
                    price=offer.price,
                    partner=offer.partner_id.name,
                ),
                user_id=offer.property_id.salesperson_id.id or self.env.user.id,
                note=_(
                    "Offer #%(id)d for %(price).0f from %(partner)s "
                    "on property '%(property)s' expires on %(deadline)s.",
                    id=offer.id,
                    price=offer.price,
                    partner=offer.partner_id.display_name,
                    property=offer.property_id.display_name,
                    deadline=offer.date_deadline,
                ),
            )
        return True
