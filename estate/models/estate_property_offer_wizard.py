from odoo import fields,models,_


class EstatePropertyOfferWizard(models.TransientModel):
    _name = 'estate.property.offer.wizard'
    _description = 'Wizard for Adding Property Offer'

    price = fields.Float(string="Offer Price", required=True)
    validity = fields.Integer(string="Validity (Days)", default=7, required=True)
    buyer_id = fields.Many2one('res.partner', string="Buyer", required=True)

    def action_make_offer(self):
        """Creates an offer for the selected properties."""
        active_ids = self.env.context.get('active_ids', [])
        properties = self.env['estate.property'].browse(active_ids)
        for property in properties:
                if property.status in ['new', 'offer_received']:
                    self.env['estate.property.offer'].create({
                        'price': self.price,
                        'validity': self.validity,
                        'partner_id': self.partner_id.id,
                        'property_id': property.id,
                    })
        return {'type': 'ir.actions.act_window_close'}
