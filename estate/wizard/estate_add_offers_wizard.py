from odoo import models, fields


class EstateAddOfferWizard(models.TransientModel):
    _name = "estate.add.offers.wizard"
    _description = "helps to add offer to multiple property at the same time"

    price = fields.Float(string='Price', required = True)
    partner_id=fields.Many2one('res.partner', string='Partner', required=True)

    def action_estate_add_offer_wizard(self):
        print("adding offer".center(100,"*"))
        active_ids = self._context.get("active_ids",[])
        property_obj = self.env['estate.property'].browse(active_ids)
        for property in property_obj:
            if property.state in ['new','offer_received']:
                vals = [{
                    'price' : self.price,
                    'partner_id': self.partner_id.id,
                    'property_id': property.id
                }]
                self.env['estate.property.offer'].create(vals)
        return True
