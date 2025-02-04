from odoo import fields, models


class EstatePropertyMakeOffer(models.TransientModel):
    _name = 'estate.property.make.offer'
    _description = "Estate Property Make Wizard"

    price = fields.Float(string="Offer Price")
    validity = fields.Integer(string="Offer Validity")
    partner_id = fields.Many2one('res.partner', string="Buyer")

    def make_offer(self):
        active_ids = self._context.get('active_ids')
        properties = self.env['estate.property'].browse(active_ids).filtered(
            lambda property: property.state in ['new', 'offer_received'])
        failed_properties = []
        offer_data = []
        for property in properties:
            try:
                if property.best_price > self.price:
                    raise ValueError(f"Best offer ({property.best_price}) is greater than {self.price}")

                offer_data.append({
                        'property_id': property.id,
                        'price': self.price,
                        'validity': self.validity,
                        'partner_id': self.partner_id.id,
                })
            except Exception as e:
                failed_properties.append(f"{property.name} ({str(e)})")
        
        if offer_data:
            self.env['estate.property.offer'].create(offer_data)

        if failed_properties:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'message': "Failed to create offers for the following properties: "
                    + ", ".join(failed_properties),
                    'type': 'danger',
                    'next': {'type': 'ir.actions.act_window_close'},
                }
            }
        return {'type': 'ir.actions.act_window_close'}
