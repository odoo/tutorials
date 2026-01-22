from odoo import api, fields, models
from datetime import timedelta
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'
    _order = 'price desc'

    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Estate Property', required=True)
    price = fields.Float()
    status = fields.Selection(
        copy=False,
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ]
    )
    property_type_id = fields.Many2one('estate.property.type', related='property_id.property_type_id', store=True, readonly=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute='_compute_date_deadline', inverse='_inverse_date_deadline', store=True)

    _check_offer_price = models.Constraint(
        'CHECK(price > 0)',
        'The offer price must be strictly positive.',
    )

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for offer in self:
            create_dt = offer.create_date if offer.create_date else fields.Datetime.now()
            offer.date_deadline = (create_dt + timedelta(days=offer.validity)).date()

    def _inverse_date_deadline(self):
        for offer in self:
            if offer.date_deadline:
                create_date = offer.create_date.date() if offer.create_date else fields.Datetime.now()
                offer.validity = (offer.date_deadline - create_date).days

    def action_confirm(self):
        for offer in self:
            if offer.property_id.state in ('offer_accepted', 'sold', 'canceled'):
                raise UserError('A sold property cannot accept new offers.')

            offer.status = 'accepted'

            offer.property_id.write({
                'buyer_id': offer.partner_id.id,
                'selling_price': offer.price,
                'state': 'offer_accepted',
            })

        return True

    def action_refuse(self):
        for offer in self:
            if offer.status == 'accepted':
                raise UserError('You cannot refuse an accepted offer.')

            offer.status = 'refused'

            property_record = offer.property_id

            active_offers = property_record.offer_ids.filtered(lambda o: o.status in ('pending', 'accepted'))

            if not active_offers:
                property_record.write({
                    'buyer_id': False,
                    'selling_price': 0,
                    'state': 'new',
                })

        return True
