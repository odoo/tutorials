from odoo import api, fields, models, exceptions


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'An offer placed on some property'

    price = fields.Float('Price')
    status = fields.Selection(
        string='Status',
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        copy=False
    )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer('Validity (days)', default=7)
    date_deadline = fields.Date('Deadline', compute='_compute_deadline', inverse='_compute_validity')

    @api.depends('validity')
    def _compute_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = fields.Date.add(record.create_date, days=record.validity)

    def _compute_validity(self):
        for record in self:
            if record.create_date and record.date_deadline:
                record.validity = (record.date_deadline - fields.Date.to_date(record.create_date)).days


    def accept_offer(self):
        for record in self:
            if record.status == 'refused':
                raise exceptions.UserError('This offer was already refused')
            if fields.Date.today() > record.date_deadline:
                raise exceptions.UserError('This offer has already expired')
            if record.property_id.buyer_id:
                raise exceptions.UserError('An offer has already been accepted')
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            record.property_id.state = 'sold'
            record.status = 'accepted'
        return True

    def reject_offer(self):
        for record in self:
            if record.status == 'accepted':
                raise exceptions.UserError('This offer was already accepted')
            record.status = 'refused'
        return True
