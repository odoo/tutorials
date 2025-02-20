import logging
from odoo import fields, models

_logger = logging.getLogger(__name__)

class EstatePropertyOfferWizard(models.TransientModel):
    _name = 'estate.property.offer.wizard'
    _description = 'Create offer'

    price = fields.Float(string="Offer", required=True)
    validity = fields.Integer(string="Validity (Days)", default=7)
    buyer_id = fields.Many2one('res.partner', string="Buyer", required=True)

    def offer_action_add(self):
        property_ids = self.env['estate.property'].browse(self._context.get('active_ids', []))
        if property_ids:
            for prop in property_ids:
                try:
                    self.env['estate.property.offer'].create({
                        'price': self.price,
                        'property_id': prop.id,
                        'validity': self.validity,
                        'buyer_id': self.buyer_id.id,
                    })
                except Exception as e:
                    _logger.warning("Cannot make offer for ", prop.name)
