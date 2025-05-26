from datetime import date, timedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate property offer'
    _order = 'price desc'

    price = fields.Float()
    status = fields.Selection(copy=False, selection=[('accepted', "Accepted"), ('refused', "Refused")])

    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    property_id = fields.Many2one('estate.property', required=True, ondelete='cascade')

    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute='_compute_date_deadline', inverse='_inverse_date_deadline')

    property_type_id = fields.Many2one(related='property_id.type_id', store=True)

    @api.depends('validity')
    def _compute_date_deadline(self):
        for offer in self:
            if offer.create_date:
                offer.date_deadline = offer.create_date + timedelta(days=offer.validity)
            else:
                offer.date_deadline = date.today() + timedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            if offer.create_date:
                offer.validity = max(0, (offer.date_deadline - offer.create_date.date()).days)
            else:
                offer.validity = max(0, (offer.date_deadline - date.today()).days)

    def accept_offer(self):
        offers_to_accept = self.filtered(lambda o: o.status != "accepted")

        for offer in offers_to_accept:
            if any(o.status == "accepted" for o in offer.property_id.offer_ids):
                raise UserError(self.env._("You can't accept more than One offer by property"))

            offer.status = 'accepted'
            offer.property_id.selling_price = offer.price
            offer.property_id.buyer_id = offer.partner_id
            offer.property_id.state = 'offer_accepted'

        return True

    def refuse_offer(self):
        for offer in self:
            offer.status = 'refused'
            offer.property_id.selling_price = 0
            offer.property_id.buyer_id = None
        return True

    _sql_constraints = [
        ('check_price_positive', 'CHECK(price >= 0)',
        "The offer price must be strictly positive")
    ]

    @api.model_create_multi
    def create(self, vals_list):
        newOffers = super().create(vals_list)
        for newOffer in newOffers:
            if newOffer.price < newOffer.property_id.best_price:
                raise UserError(self.env._("The offer price cannot be lower than the highest existing"))
            else:
                if newOffer.property_id.state == 'new':
                    newOffer.property_id.state = 'offer_received'
        return newOffers
