from odoo import fields, models


class EstatePropertyOffer(models.Model):
    _inherit = 'estate.property.offer'

    offer_lead_id = fields.Many2one('crm.lead')

    def create(self, vals_list):
        offers = super().create(vals_list)
        for offer in offers:
            offer_lead = self.env['crm.lead'].create({
                'name': 'Offer lead from %s ' % offer.property_id.name,
                'partner_id': offer.partner_id.id,
                'user_id': offer.property_id.salesperson_id.id,
                'team_id': False,
                'description': 'offferss',
                'referred': False,
                'source_id': False,
            })
            offers.offer_lead_id = offer_lead.id
        return offers

    def action_accept(self):
        offer = super().action_accept()
        if self.offer_lead_id:
            self.offer_lead_id.action_set_won()
        return offer

    def action_refuse(self):
        offer = super().action_refuse()
        if self.offer_lead_id:
            self.offer_lead_id.action_set_lost()
        return offer
