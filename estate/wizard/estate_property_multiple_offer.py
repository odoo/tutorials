from odoo import fields, models


class EstatePropertyMultipleOffer(models.TransientModel):
    _name = "estate.property.multiple.offer"
    _description = "Offer for multiple properties"

    price = fields.Float(string="Price")
    partner_id = fields.Many2one('res.partner', string="Buyer", required=True)

    def action_add_multiple_offers(self):
        active_ids = self._context.get('active_ids', [])
        property_obj = self.env['estate.property'].browse(active_ids)
        for property in property_obj:
            if property.state in ['new', 'offer_received']:
                val = [{
                    'price' : self.price,
                    'partner_id' : self.partner_id.id,
                    'property_id' : property.id
                }]
                self.env['estate.property.offer'].create(val)
        return True
