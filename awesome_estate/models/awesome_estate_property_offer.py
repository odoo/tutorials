from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class AwesomeEstatePropertyOffer(models.Model):
    _name = 'awesome.estate.property.offer'
    _description = 'Real Estate Property Offer'
    _order = 'price desc, id desc'

    price = fields.Float()
    status = fields.Selection(
        [
            ('accepted', "Accepted"),
            ('refused', "Refused"),
        ],
        copy=False,
    )
    partner_id = fields.Many2one(
        'res.partner',
        string="Buyer",
        required=True,
    )
    property_id = fields.Many2one(
        'awesome.estate.property',
        string="Property",
        required=True,
        ondelete='cascade',
        index=True,
    )
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute='_compute_date_deadline',
        inverse='_inverse_date_deadline',
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

    def action_accept(self):
        self.ensure_one()
        if self.status:
            raise UserError("This offer has already been accepted or refused.")
        if self.property_id.state == 'cancelled':
            raise UserError("Cannot accept offers on cancelled properties.")
        existing_accepted = self.search([
            ('property_id', '=', self.property_id.id),
            ('status', '=', 'accepted'),
        ])
        if existing_accepted:
            raise UserError(
                "Another offer on this property has already been accepted. "
                "Only one offer can be accepted per property."
            )
        (self.property_id.offer_ids - self).write({'status': 'refused'})
        self.status = 'accepted'
        self.property_id.write({
            'selling_price': self.price,
            'buyer_id': self.partner_id.id,
            'state': 'offer_accepted',
        })
        return True

    def action_refuse(self):
        self.ensure_one()
        if self.status:
            raise UserError("This offer has already been accepted or refused.")
        if self.property_id.state == 'cancelled':
            raise UserError("Cannot refuse offers on cancelled properties.")
        self.status = 'refused'
        return True

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_id = vals.get('property_id')
            new_price = vals.get('price', 0)
            if property_id:
                property = self.env['awesome.estate.property'].browse(property_id)
                if property.state == 'cancelled':
                    raise UserError("Cannot create offers on a cancelled property.")
            if property_id and new_price:
                existing_offers = self.search([
                    ('property_id', '=', property_id),
                ])
                if existing_offers:
                    max_price = max(existing_offers.mapped('price'))
                    if new_price <= max_price:
                        raise ValidationError(
                            f"Offer must be higher than the highest existing "
                            f"offer (${max_price:,.2f})."
                        )
        offers = super().create(vals_list)
        for offer in offers:
            if offer.property_id.state == 'new':
                offer.property_id.state = 'offer_received'
        return offers
