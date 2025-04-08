from dateutil.relativedelta import relativedelta
from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'An offer made for an Estate Property'

    price = fields.Float('Price')
    validity = fields.Integer('Validity (days)', default=7)
    status = fields.Selection(
        [('accepted', 'Accepted'), ('refused', 'Refused')], copy=False
    )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    date_deadline = fields.Date(
        'Deadline', compute='_compute_date_deadline', inverse='_inverse_date_deadline'
    )

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = (
                record.create_date or fields.Date.today()
            ) + relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (
                relativedelta(
                    record.date_deadline, (record.create_date or fields.Date.today())
                ).days
                + 1
            )

    def action_accept(self):
        for record in self:
            record_property = record.property_id
            if record_property.state == 'offer_accepted':
                raise UserError('You can only accept one offer at a time.')

            record.status = 'accepted'
            record_property.update({
                'buyer_id': record.partner_id.id,
                'selling_price': record.price,
                'state': 'offer_accepted',
            })
        return True

    def action_refuse(self):
        for record in self:
            record.status = 'refused'
            record.property_id.state = 'offer_received'
        return True
