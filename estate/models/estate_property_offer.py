from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Offer for an estate property'
    _order = 'price desc'

    price = fields.Float()
    status = fields.Selection(copy=False, selection=[('accepted', 'Accepted'), ('refused', 'Refused')])
    validity = fields.Integer(string='Validity (days)', default=7)
    date_deadline = fields.Date(string='Deadline', compute='_compute_deadline', inverse='_inverse_deadline')

    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    property_type_id = fields.Many2one(related='property_id.property_type_id', store=True)

    _price_gt_zero = models.Constraint(
        'CHECK(price>0)', 'An offer price must be strictly positive',
    )

    @api.depends('validity', 'create_date')
    def _compute_deadline(self):
        for offer in self:
            create_date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.date_deadline = create_date + relativedelta(days=offer.validity)

    def _inverse_deadline(self):
        for offer in self:
            offer.validity = (offer.date_deadline - offer.create_date.date()).days

    def action_accept_offer(self):
        for offer in self:
            if 'accepted' in offer.mapped("property_id.offer_ids.status"):
                raise UserError("Only one offer can be accepeted !")
            offer.status = 'accepted'
            offer.property_id.buyer_id = offer.partner_id
            offer.property_id.selling_price = offer.price
            offer.property_id.state = 'offer_accepted'
            (offer.property_id.offer_ids - offer).write({'status': 'refused'})
        return True

    def action_refuse_offer(self):
        for offer in self:
            if offer.status == 'accepted':
                offer.property_id.buyer_id = False
                offer.property_id.selling_price = False
                offer.property_id.state = 'offer_received'
            offer.status = 'refused'
        return True
