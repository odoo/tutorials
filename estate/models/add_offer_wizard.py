from odoo import models, fields, api

class AddOfferWizard(models.TransientModel):
    _name = 'add.offer.wizard'
    _description = 'Add Offer Wizard'

    price = fields.Float('Price', default=500000.0, required=True)
    validity = fields.Integer('Validity')
    buyer_id = fields.Many2one('res.partner', string="Buyer", required=True)
    property_ids = fields.Many2many('estate.property', string="Properties")

    # @api.model_create_multi
    def action_make_offer(self):
        for property in self.property_ids:
            self.env['estate.property.offer'].create({
                'price': self.price,
                'validity': self.validity,
                'partner_id': self.buyer_id.id,
                'property_id': property.id
            })
        return {'type': 'ir.actions.act_window_close'}
