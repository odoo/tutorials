from odoo import api, models, fields
from dateutil.relativedelta import relativedelta


class EstateAddOfferWizard(models.TransientModel):
    _name = 'estate.add.offer.wizard'
    _description = 'Wizard to add offer to properties'

    property_ids = fields.Many2many('estate.property', string='Properties')
    partner_id = fields.Many2one('res.partner', string='Buyer', required=True)
    price = fields.Float(string='Offer Price', required=True)
    current_date = fields.Date.today()
    date = current_date + relativedelta(days=7)
    date_deadline = fields.Date(string="Date Deadline", default=date)

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        res['property_ids'] = self.env.context.get('active_ids', [])
        return res

    def action_add_offers(self):
        for prop in self.property_ids:
            self.env['estate.property.offer'].create({
                'property_id': prop.id,
                'partner_id': self.partner_id.id,
                'price': self.price,
            })
        return {'type': 'ir.actions.act_window_close'}
