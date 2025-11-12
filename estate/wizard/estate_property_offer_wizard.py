import logging
from odoo import fields, models

_logger = logging.getLogger(__name__)

class EstatePropertyOfferWizard(models.TransientModel):
    _name = 'estate.property.offer.wizard'
    _description = 'Make offer'

    price = fields.Float(string="Offer", required=True)
    partner_id = fields.Many2one(comodel_name='res.partner', string="Partner", required=True)
    validity = fields.Integer(string="Validity (Days)", default=7)

    def action_create_offers(self):
        active_ids = self.env.context.get('active_ids', [])
        property_model = self.env['estate.property']
        offer_model = self.env['estate.property.offer']

        if active_ids:
            properties = property_model.browse(active_ids)
            for property in properties:
                try:
                    offer_model.create({
                        'property_id': property.id,
                        'price': self.price,
                        'partner_id': self.partner_id.id,
                    })
                except Exception as e:
                    _logger.warning("Cannot make offer for %s", property.name)
