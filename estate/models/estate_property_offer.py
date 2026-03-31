from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real estate system - Property Offer"

    price = fields.Float(string="Offer Price")
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused')
    ], copy=False)

    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True, ondelete='cascade')

    validity = fields.Integer(default=7)

    date_deadline = fields.Date(
        compute='_compute_date_deadline',
        inverse='_inverse_date_deadline'
    )

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for offer in self:
            date = offer.create_date or fields.Date.today()
            offer.date_deadline = date + timedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for record in self:
            start = record.create_date.date() if record.create_date else fields.Date.today()
            record.validity = (record.date_deadline - start).days

    def action_accept_offer(self):
        if self.property_id.state in ('sold', 'cancelled'):
            raise UserError("Cannot accept an offer on a sold or cancelled property.")
        if self.property_id.offer_ids.filtered(lambda offer: offer.status == 'accepted'):
            raise UserError("An offer is already accepted for this property.")
        for offer in self.property_id.offer_ids:
            if offer.id != self.id:
                offer.status = 'refused'
        self.status = 'accepted'
        self.property_id.selling_price = self.price
        self.property_id.buyer_id = self.partner_id.id
        self.property_id.state = 'offer_accepted'
        return True

    def action_refuse_offer(self):
        if self.property_id.state in ('sold', 'cancelled'):
            raise UserError("Cannot refuse an offer on a sold or cancelled property.")
        if self.status == 'accepted':
            raise UserError("Cannot refuse an accepted offer.")
        self.status = 'refused'
        return True

    @api.ondelete(at_uninstall=False)
    def _on_offer_unlink(self):
        for offer in self:
            if offer.status == 'accepted':
                offer.property_id.selling_price = 0
                offer.property_id.state = 'offer_received'
