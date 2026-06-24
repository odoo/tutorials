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
        _('The offer price must be strictly positive.'),
    )

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
                delta = fields.Date.to_date(record.date_deadline) - fields.Date.to_date(record.create_date)
                record.validity = delta.days
            elif record.date_deadline:
                delta = fields.Date.to_date(record.date_deadline) - fields.Date.today()
                record.validity = delta.days if delta.days > 0 else 0

    # -----------------------------------------------------------------------
    # CRUD Methods
    # -----------------------------------------------------------------------
    def _accept_process(self, offer):
        """Accept an offer: refuse other offers, update property selling price, buyer, and state."""
        (offer.property_id.offer_ids - offer).write({'status': 'refused'})
        offer.property_id.write({
            'selling_price': offer.price,
            'buyer_id': offer.partner_id.id,
            'state': 'offer_accepted',
        })

    def write(self, vals):
        # Catch all status changes from the editable list dropdown.
        # The inline list calls write() directly (bypassing action_* methods),
        # so we replicate the business logic here.
        if 'status' in vals and vals['status'] is not False:
            for offer in self:
                # Once an offer has a status (accepted or refused), it is final.
                # Block any further status change, regardless of direction.
                if offer.status:
                    raise UserError(
                        _("This offer has already been accepted or refused.")
                    )
                if vals['status'] == 'accepted':
                    if offer.property_id.state == 'canceled':
                        raise UserError(
                            _("Cannot accept offers on canceled properties.")
                        )
                    existing_accepted = self.search([
                        ('property_id', '=', offer.property_id.id),
                        ('status', '=', 'accepted'),
                    ])
                    if existing_accepted:
                        raise UserError(
                            _("Another offer on this property has already been "
                              "accepted. Only one offer can be accepted per property.")
                        )
                    self._accept_process(offer)
        return super().write(vals)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_id = vals.get('property_id')
            new_price = vals.get('price', 0)
            if property_id:
                property = self.env['awesome.estate.property'].browse(property_id)
                if property.state == 'canceled':
                    raise ValidationError(_("Cannot create offers on a canceled property."))
            if property_id and new_price:
                existing_offers = self.search([
                    ('property_id', '=', property_id),
                ])
                if existing_offers:
                    max_price = max(existing_offers.mapped('price'))
                    if new_price <= max_price:
                        raise ValidationError(
                            _("Offer must be higher than the highest existing offer ($%.2f).") % max_price
                        )
        offers = super().create(vals_list)
        for offer in offers:
            if offer.property_id.state == 'new':
                offer.property_id.state = 'offer_received'
        return offers

    # -----------------------------------------------------------------------
    # Action Methods
    # -----------------------------------------------------------------------
    def action_accept(self):
        self.ensure_one()
        if self.status:
            raise UserError(_("This offer has already been accepted or refused."))
        if self.property_id.state == 'canceled':
            raise UserError(_("Cannot accept offers on canceled properties."))
        existing_accepted = self.search([
            ('property_id', '=', self.property_id.id),
            ('status', '=', 'accepted'),
        ])
        if existing_accepted:
            raise UserError(
                _("Another offer on this property has already been accepted. "
                  "Only one offer can be accepted per property.")
            )
        self._accept_process(self)
        self.status = 'accepted'
        return True

    def action_refuse(self):
        self.ensure_one()
        if self.status:
            raise UserError(_("This offer has already been accepted or refused."))
        if self.property_id.state == 'canceled':
            raise UserError(_("Cannot refuse offers on canceled properties."))
        self.status = 'refused'
        return True
