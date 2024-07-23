from odoo import models, fields
from dateutil.relativedelta import relativedelta


class PropertyOffer(models.TransientModel):
    _name = 'estate.property.offer.wizard'
    _description = 'Property Offer Wizard'

    price = fields.Float(string='Offer Price')
    buyer_id = fields.Many2one('res.partner', string='Buyer')
    deadline_date = fields.Date(string='Deadline Date', default=lambda self: fields.Date.today() + relativedelta(days=7))

    def make_offer(self):
        properties = self.env['estate.property'].browse(self.env.context.get('active_ids', []))
        for props in properties:
            self.env['estate.property.offer'].create({
                'price': self.price,
                'partner_id': self.buyer_id.id,
                'property_id': props.id,
                'date_deadline': self.deadline_date
            })
        return {'type': 'ir.actions.act_window_close'}
