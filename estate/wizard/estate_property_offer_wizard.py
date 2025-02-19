from odoo import models, fields, api

class EstatePropertyOfferWizard(models.TransientModel):
    _name = "estate.property.offer.wizard"

    price = fields.Float(string='Offer Price')
    validity = fields.Integer(string='Validity',default=7)
    buyer = fields.Many2one('res.partner', string='Buyer')
    property_ids = fields.Many2many('estate.property', string='Properties')
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)

    @api.model_create_multi
    def default_get(self, fields):
        res = super(EstatePropertyOfferWizard, self).default_get(fields)
        active_ids = self.env.context.get('active_ids', [])
        if active_ids:
            res.update({'property_ids': [(6, 0, active_ids)]})
        return res

    def make_offer(self):
        for property in self.property_ids:
            self.env['estate.property.offer'].create({
                'property_id': property.id,
                'price': self.price,
                'validity': self.validity,
                'partner_id': self.partner_id.id,
            })
        return {'type': 'ir.actions.act_window_close'}

    def cancel_offer(self):
        return {'type': 'ir.actions.act_window_close'}

