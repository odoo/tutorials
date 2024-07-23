from odoo import fields, models, api
from dateutil.relativedelta import relativedelta


class AddOfferWizard(models.TransientModel):
    _name = 'estate.property.add.offer.wizard'
    _description = 'Wizard to Add Offers to Multiple Properties'

    property_ids = fields.Many2many('estate.property', string='Properties')
    partner_id = fields.Many2one('res.partner', string='Buyer', required=True)
    price = fields.Float(string='Offer Price', required=True)
    current_date = fields.Date.today()
    date = current_date + relativedelta(days=7)
    date_deadline = fields.Date(string="Date Deadline", default=date, readonly=True)

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        res['property_ids'] = self.env.context.get('active_ids', [])
        return res

    def action_add_offers(self):
        for proper in self.property_ids:
            self.env['estate.property.offer'].create({
                'property_id': proper.id,
                'partner_id': self.partner_id.id,
                'price': self.price,
            })
        return {'type': 'ir.actions.act_window_close'}
