from odoo import models, fields
from odoo.exceptions import UserError


class EstateAddOfferWizard(models.TransientModel):
    _name = 'estate.add.offer.wizard'
    _description = 'Add Offer Wizard'

    price = fields.Float(string="Offer Price", required=True)
    offer_status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused')
    ], string="Offer Status")
    buyer_id = fields.Many2one('res.partner', string="Buyer", required=True)

    def action_add_offer(self):
        active_ids = self.env.context.get('active_ids')
        properties = self.env['estate.property'].browse(active_ids).filtered(
            lambda p: p.expected_price <= self.price
        ).filtered(
            lambda q: q.property_type_id.name == 'House'
        )
        for p in properties:
            if p.state in ['new', 'offer_received']:
                p.offer_ids.create({
                    'property_id': p.id,
                    'price': self.price,
                    'partner_id': self.buyer_id.id
                })
            else:
                raise UserError('Property must be in new or offer received state')
        return {'type': 'ir.actions.act_window_close'}
