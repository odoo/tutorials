from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class AwesomeEstatePropertyOffer(models.Model):
    _name = 'awesome.estate.property.offer'
    _description = 'Real Estate Property Offer'
    _order = 'price desc, id desc'

    # -----------------------------------------------------------------------
    # Fields
    # -----------------------------------------------------------------------
    price = fields.Float()
    status = fields.Selection(
        [
            ('accepted', "Accepted"),
            ('refused', "Refused"),
        ],
        string="Status",
        copy=False,
    )
    partner_id = fields.Many2one(
        'res.partner',
        string="Partner",
        required=True,
        index=True,
    )
    property_id = fields.Many2one(
        'awesome.estate.property',
        string="Property",
        required=True,
        ondelete='cascade',
        index=True,
    )
    property_type_id = fields.Many2one(
        'awesome.estate.property.type',
        string="Property Type",
        related='property_id.property_type_id',
        store=True,
    )
    validity = fields.Integer(
        string="Validity (days)",
        default=7,
    )
    # Bidirectional date link (tutorial Ch.8 / community compute+inverse pattern):
    # - compute: validity days → absolute deadline date
    # - inverse: user edits deadline → rewrite validity as day delta
    date_deadline = fields.Date(
        string="Deadline",
        compute='_compute_date_deadline',
        inverse='_inverse_date_deadline',
        store=True,
    )
    is_suspicious = fields.Boolean(
        string="Suspicious",
        default=False,
        copy=False,
        help="Set automatically when the same partner places 2+ offers "
             "within 5 minutes. Can also be set or cleared manually.",
    )

    # -----------------------------------------------------------------------
    # SQL Constraints
    # -----------------------------------------------------------------------
    _check_offer_price = models.Constraint(
        'CHECK (price > 0)',
        'The offer price must be strictly positive.',
    )
    _check_offer_price_max = models.Constraint(
        'CHECK (price <= 9999999999)',
        'The offer price seems unreasonably high.',
    )

    # -----------------------------------------------------------------------
    # Python Constraints
    # -----------------------------------------------------------------------
    @api.constrains('validity')
    def _check_validity_positive(self):
        for record in self:
            if record.validity <= 0:
                raise ValidationError(
                    _("Validity must be a positive number of days."),
                )

    # -----------------------------------------------------------------------
    # Compute Methods
    # -----------------------------------------------------------------------
    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        """Deadline = creation date + validity days."""
        for record in self:
            if record.create_date:
                record.date_deadline = fields.Date.add(
                    fields.Date.to_date(record.create_date), days=record.validity,
                )
            else:
                record.date_deadline = fields.Date.add(
                    fields.Date.today(), days=record.validity,
                )

    # -----------------------------------------------------------------------
    # Inverse Methods
    # -----------------------------------------------------------------------
    def _inverse_date_deadline(self):
        """User edited deadline → recompute validity."""
        for record in self:
            if record.date_deadline and record.create_date:
                deadline = fields.Date.to_date(record.date_deadline)
                created = fields.Date.to_date(record.create_date)
                if deadline < created:
                    raise ValidationError(
                        _("The deadline date cannot be before the offer creation date."),
                    )
                record.validity = (deadline - created).days
            elif record.date_deadline:
                deadline = fields.Date.to_date(record.date_deadline)
                today = fields.Date.today()
                if deadline < today:
                    raise ValidationError(
                        _("The deadline date must be after today."),
                    )
                record.validity = (deadline - today).days

    # -----------------------------------------------------------------------
    # CRUD Methods
    # -----------------------------------------------------------------------
    @api.model_create_multi
    def create(self, vals_list):
        """Create property offers.

        Skip property state and price escalation guards during module data
        loading (demo/seed data) so that XML data files can seed records
        without hitting business-rule validations.  This follows the
        established pattern from enterprise/account_3way_match.
        """
        if not self.env.context.get('module'):
            for vals in vals_list:
                property_id = vals.get('property_id')
                new_price = vals.get('price', 0)
                if property_id:
                    estate_property = self.env['awesome.estate.property'].browse(
                        property_id)
                    if estate_property.state in ('sold', 'canceled', 'offer_accepted'):
                        raise ValidationError(
                            _("Cannot create offers on a property that is %s.",
                              estate_property.state),
                        )
                if property_id and new_price > 0:
                    existing_offers = self.search([
                        ('property_id', '=', property_id),
                    ])
                    if existing_offers:
                        max_price = max(existing_offers.mapped('price'))
                        if new_price <= max_price:
                            raise ValidationError(
                                _("Offer must be higher than the highest existing offer ($%.2f).", max_price),
                            )
        offers = super().create(vals_list)
        offers._flag_duplicate_offers()
        for offer in offers:
            if offer.property_id.state == 'new':
                offer.property_id.state = 'offer_received'
        return offers

    # -----------------------------------------------------------------------
    # Action Methods
    # -----------------------------------------------------------------------
    def action_accept(self):
        """Accept this offer: update property, refuse other pending offers."""
        self.ensure_one()
        if self.is_suspicious:
            raise UserError(
                _("Cannot accept a suspicious offer. Clear the flag first "
                  "if this offer is legitimate.")
            )
        if self.status:
            raise UserError(
                _("This offer has already been accepted or refused."))
        if self.property_id.state in ('sold', 'canceled', 'offer_accepted'):
            raise UserError(
                _("Cannot accept offers on a property that is %s.",
                  self.property_id.state),
            )
        existing_accepted = self.search([
            ('property_id', '=', self.property_id.id),
            ('status', '=', 'accepted'),
            ('id', '!=', self.id),
        ])
        if existing_accepted:
            raise UserError(
                _("Another offer has already been accepted for this property."))
        other_offers = self.property_id.offer_ids - self
        other_offers.filtered(lambda o: not o.status).write(
            {'status': 'refused'})
        self.property_id.with_context(accepting_offer=True).write({
            'selling_price': self.price,
            'buyer_id': self.partner_id.id,
            'state': 'offer_accepted',
        })
        return super().write({'status': 'accepted'})

    def action_refuse(self):
        """Refuse this offer. Only pending offers can be refused."""
        self.ensure_one()
        if self.status:
            raise UserError(
                _("This offer has already been accepted or refused."))
        self.status = 'refused'
        return True

    def action_mark_suspicious(self):
        """Manually mark this offer as suspicious."""
        self.ensure_one()
        if self.status:
            raise UserError(
                _("Cannot mark a %s offer as suspicious.", self.status)
            )
        if self.is_suspicious:
            raise UserError(_("This offer is already marked as suspicious."))
        self.is_suspicious = True
        return True

    def action_clear_suspicious(self):
        """Clear the suspicious flag."""
        self.ensure_one()
        if self.status:
            raise UserError(
                _("Cannot clear the suspicious flag on a %s offer.", self.status)
            )
        if not self.is_suspicious:
            raise UserError(_("This offer is not marked as suspicious."))
        self.is_suspicious = False
        return True

    # -----------------------------------------------------------------------
    # Business / Helper Methods
    # -----------------------------------------------------------------------
    def _flag_duplicate_offers(self):
        """Flag offers from the same partner on the same property within 5 minutes."""
        for offer in self:
            if not offer.partner_id or not offer.property_id or not offer.create_date:
                continue
            before = fields.Datetime.add(offer.create_date, minutes=-5)
            duplicates = self.search([
                ('partner_id', '=', offer.partner_id.id),
                ('property_id', '=', offer.property_id.id),
                ('create_date', '>=', before),
                ('id', '!=', offer.id),
            ])
            if duplicates:
                (offer | duplicates).write({'is_suspicious': True})

    # -----------------------------------------------------------------------
    # Cron Methods
    # -----------------------------------------------------------------------
    @api.model
    def _cron_refuse_expired_offers(self):
        """Daily cron: refuse offers past their deadline.

        Only affects offers with a deadline date before today that are
        still pending (no accepted/refused status set).
        """
        expired_offers = self.search([
            ('date_deadline', '<', fields.Date.today()),
            ('status', 'not in', ['accepted', 'refused']),
        ])
        if expired_offers:
            expired_offers.write({'status': 'refused'})
        return True
