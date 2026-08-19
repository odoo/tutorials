from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer Model'

    price = fields.Float()
    status = fields.Selection(
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
        copy=False,
    )
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(string='Deadline', compute='_compute_date_deadline', inverse='_inverse_date_deadline')

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            create_date = fields.Date.today()
            if record.create_date:
                create_date = record.create_date.date()

            record.date_deadline = create_date + relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            create_date = fields.Date.today()
            if record.create_date:
                create_date = record.create_date.date()

            record.validity = (record.date_deadline - create_date).days

    def action_accept(self):
        CANNOT_ACCEPT_ACCEPTED_OFFER = "You cannot accept an offer for a property that already has an accepted offer"
        if self.property_id.state == 'offer_accepted':
            raise UserError(CANNOT_ACCEPT_ACCEPTED_OFFER)

        self.status = 'accepted'
        self.property_id.state = 'offer_accepted'
        self.property_id.selling_price = self.price
        self.property_id.buyer_id = self.partner_id

    def action_refuse(self):
        CANNOT_REFUSE_ACCEPTED_OFFER = "You cannot refuse an accepted offer"
        if self.status == 'accepted':
            raise UserError(CANNOT_REFUSE_ACCEPTED_OFFER)
        self.status = 'refused'
