from odoo import api, fields, models


class EstateOfferWizard(models.TransientModel):
    _name = "estate.offer.wizard"
    _description = "Create Offer for Multiple Properties"

    price = fields.Float(string="Offer Price", required=True)
    validity = fields.Integer(string="Validity (Days)", default=7, required=True)
    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)

    def action_make_offer(self):
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
