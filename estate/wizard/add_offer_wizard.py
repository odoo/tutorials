from odoo import fields, models
from odoo.exceptions import UserError


class AddOfferWizard(models.TransientModel):
    _name = 'estate.add.offer.wizard'
    _description = 'Add Offer Wizard'

    price = fields.Float('Price', required=True)
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused')
    ])
    buyer_id = fields.Many2one('res.partner', string='Buyer', required=True)

    def add_offer(self):
        active_ids = self.env.context.get('active_ids')
        properties = self.env['estate.property'].browse(active_ids).filtered(lambda p: p.expected_price <= self.price)

        for prop in properties:
            if prop.state == 'new' or prop.state == 'offer_received':
                curr = prop.offer_ids.create({
                'property_id': prop.id,
                'price': self.price,
                'partner_id': self.buyer_id.id
            })
            if self.status == 'accepted':
                curr.action_accepted()
            elif self.status == 'refused':
                curr.action_refused()
            else:
                raise UserError('Property must be in new or offer received state')

        return {'type': 'ir.actions.act_window_close'}
