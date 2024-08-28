from odoo import models, fields


class EstateAddOfferWizard(models.TransientModel):

    _name = "estate.add.offer.wizard"
    _description = "Estate Add Offer Wizard"

    price = fields.Float(string='Price')
    offer_status = fields.Selection(string='Offer Status',
                                    selection=[
                                        ('accepted', 'Accepted'),
                                        ('refused', 'Refused')
                                    ])
    buyer = fields.Many2one('res.partner', string='Buyer')

    def make_an_offer(self):
        active_ids = self._context.get('active_ids', [])
        properties = self.env['estate.property'].browse(active_ids)
        for estate_property in properties:
            self.env['estate.property.offer'].create({
                'property_id': estate_property.id,
                'price': self.price,
                'status': self.offer_status,
                'partner_id': self.buyer.id
            })
        return {'type': 'ir.actions.act_window_close'}
