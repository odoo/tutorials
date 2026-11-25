from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'
    _order = 'price desc'

    price = fields.Float()
    status = fields.Selection(
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused')
        ],
        copy=False
    )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer('Validity (Days)', default=7)
    date_deadline = fields.Date('Deadline', compute='_compute_date_deadline', inverse='_inverse_date_deadline')
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)

    _check_price_positive = models.Constraint(
        'CHECK(price > 0)',
        'The offer for the property must be strictly positive'
    )

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            base_date = record.create_date.date() if record.create_date else fields.Date.context_today(record)
            record.date_deadline = base_date + relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline:
                base_date = record.create_date.date() if record.create_date else fields.Date.context_today(record)
                record.validity = (record.date_deadline - base_date).days

    def action_accept_offer(self):
        print("yes i did it hourraaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        for record in self:
            if record.property_id.state not in ('new', 'offer_received'):
                raise UserError(self.env._('You cannot accept offers for sold, cancelled and accepted properties.'))
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            record.property_id.state = 'offer_accepted'
            record.status = 'accepted'

            offers_pending = record.property_id.offer_ids.filtered(lambda offer: not offer.status)
            offers_pending.write({'status': 'refused'})

    def action_refuse_offer(self):
        self.status = 'refused'

    @api.model
    def create(self, vals_list):
        for vals in vals_list:
            prop = self.env['estate.property'].browse(vals['property_id'])
            if prop.offer_ids:
                max_offer = prop.best_price
                if float_compare(vals['price'], max_offer, precision_rounding=0.01) <= 0:
                    raise ValidationError(self.env._('The amount must be higher than %s.', max_offer))
            prop.state = 'offer_received'
        return super().create(vals_list)
