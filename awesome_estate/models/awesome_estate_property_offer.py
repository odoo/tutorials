from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class AwesomeEstatePropertyOffer(models.Model):
    _name = 'awesome.estate.property.offer'
    _description = 'Real Estate Property Offer'
    _order = 'price desc, id desc'

    price = fields.Float(string="Price")
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
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(
        string="Deadline",
        compute='_compute_date_deadline',
        inverse='_inverse_date_deadline',
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
                    _("Validity must be a positive number of days.")
                )

    # -----------------------------------------------------------------------
    # Computed Fields & Inverse
    # -----------------------------------------------------------------------
    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = fields.Date.add(
                    fields.Date.to_date(record.create_date), days=record.validity,
                )
            else:
                record.date_deadline = fields.Date.add(
                    fields.Date.today(), days=record.validity,
                )

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline and record.create_date:
                deadline = fields.Date.to_date(record.date_deadline)
                created = fields.Date.to_date(record.create_date)
                if deadline < created:
                    raise ValidationError(
                        _("The deadline date cannot be before the offer creation date.")
                    )
                record.validity = (deadline - created).days
            elif record.date_deadline:
                deadline = fields.Date.to_date(record.date_deadline)
                today = fields.Date.today()
                if deadline <= today:
                    raise ValidationError(
                        _("The deadline date must be after today.")
                    )
                record.validity = (deadline - today).days

    # -----------------------------------------------------------------------
    # CRUD Methods
    # -----------------------------------------------------------------------
    def write(self, vals):
        # Lightweight guard: block changing to a *different* status once set.
        # Prevents corrupting an accepted/refused offer via inline editable list.
        # Clearing to False is always allowed (resets from action_reset()).
        # The 'force_refuse' context bypass allows property cancellation to work.
        if 'status' in vals and vals.get('status') and not self.env.context.get('force_refuse'):
            for offer in self:
                if offer.status and vals.get('status') != offer.status:
                    raise UserError(
                        _("This offer has already been accepted or refused.")
                    )
                if vals['status'] == 'accepted':
                    # Guard: property must be accept-able
                    if offer.property_id.state in ('sold', 'canceled', 'offer_accepted'):
                        raise UserError(
                            _("Cannot accept offers on a property that is %s.", offer.property_id.state)
                        )
                    # Guard: no other accepted offer exists for this property
                    existing_accepted = self.search([
                        ('property_id', '=', offer.property_id.id),
                        ('status', '=', 'accepted'),
                        ('id', '!=', offer.id if offer.id else False),
                    ])
                    if existing_accepted:
                        raise UserError(_("Another offer has already been accepted for this property."))
                    self._accept_process(offer)
        return super().write(vals)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_id = vals.get('property_id')
            new_price = vals.get('price', 0)
            if property_id:
                property = self.env['awesome.estate.property'].browse(property_id)
                if property.state in ('sold', 'canceled', 'offer_accepted'):
                    raise ValidationError(
                        _("Cannot create offers on a property that is %s.", property.state)
                    )
            if property_id and new_price > 0:
                existing_offers = self.search([
                    ('property_id', '=', property_id),
                ])
                if existing_offers:
                    max_price = max(existing_offers.mapped('price'))
                    if new_price <= max_price:
                        raise ValidationError(
                            _("Offer must be higher than the highest existing offer ($%.2f).", max_price)
                        )
        offers = super().create(vals_list)
        for offer in offers:
            if offer.property_id.state == 'new':
                offer.property_id.state = 'offer_received'
        return offers

    # -----------------------------------------------------------------------
    # Helper Methods
    # -----------------------------------------------------------------------
    def _accept_process(self, offer):
        """Shared accept logic: update property, refuse other offers.

        Called by both action_accept() and write() to ensure the same
        business logic runs regardless of the entry path.
        """
        # Auto-refuse only the *other undecided* offers (skip already-processed)
        other_offers = offer.property_id.offer_ids - offer
        other_offers.filtered(lambda o: not o.status).write({'status': 'refused'})
        # Update the property with the accepted offer details
        offer.property_id.write({
            'selling_price': offer.price,
            'buyer_id': offer.partner_id.id,
            'state': 'offer_accepted',
        })

    # -----------------------------------------------------------------------
    # Action Methods
    # -----------------------------------------------------------------------
    def action_accept(self):
        """Accept this offer, delegating all logic and guards to write()."""
        self.ensure_one()
        if self.status:
            raise UserError(_("This offer has already been accepted or refused."))
        self.with_context(accepting_offer=True).write({'status': 'accepted'})
        return True

    def action_refuse(self):
        self.ensure_one()
        if self.status and not self.env.context.get('force_refuse'):
            raise UserError(_("This offer has already been accepted or refused."))
        self.status = 'refused'
        return True
