from dateutil.relativedelta import relativedelta
from datetime import date

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'for adding offers of properties'
    _order = 'price desc'

    price=fields.Float(string='Price')
    status=fields.Selection(
        string='Status',
        selection=[
            ('accepted','Accepted'),
            ('refused','Refused')
        ],
        copy=False
    )
    partner_id=fields.Many2one('res.partner', string='Partner', required=True)
    property_id=fields.Many2one('estate.property', string='Property', required=True)
    validity = fields.Integer(string='Validity (days)', default=7,)
    date_deadline = fields.Date(string='Deadline', compute='_compute_date_deadline', inverse='_inverse_date_deadline')
    property_type_id = fields.Many2one(related='property_id.property_type_id', store=True)

    _sql_constraints = [
        ('offer_price_check','CHECK( price >= 0 )', 'An offer price must be strictly positive')
    ]

    @api.depends('create_date','validity')
    def _compute_date_deadline(self):
        for offer in self:
            if offer.create_date:
                offer.date_deadline = offer.create_date.date() + relativedelta(days=offer.validity)
            else:
                offer.date_deadline = date.today() + relativedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            if offer.create_date and offer.date_deadline:
                offer.validity = (offer.date_deadline - offer.create_date.date()).days

    def action_offer_accept_btn(self):
        for offer in self:
            if offer.property_id.offer_ids.filtered(lambda offer: offer.status=='accepted'):
                raise UserError(_('Already one offer is accepted'))
            offer.status = 'accepted'
            offer.property_id.selling_price = offer.price
            offer.property_id.buyer = offer.partner_id
            offer.property_id.state = 'offer_accepted'
        return True

    def action_offer_reject_btn(self):
        for offer in self:
            offer.status = 'refused'
            offer.property_id.selling_price = 0
            offer.property_id.buyer = False
            offer.property_id.state = 'offer_received'
        return True
