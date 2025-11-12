import logging

from odoo import models, fields


_logger = logging.getLogger(__name__)

class EstateAddPropertyOffer(models.TransientModel):
    _name = 'estate.add.property.offer'
    _description = 'Wizard to Add offer to multiple properties'

    price = fields.Float('Price')
    validity = fields.Integer('Validity (days)', default='7')
    partner_id = fields.Many2one(
        comodel_name='res.partner', required=True)

    def action_add_offer(self):
        property_ids = self.env['estate.property'].browse(self._context.get('active_ids', []))
        if property_ids:
            for property in property_ids:
                try:
                    self.env['estate.property.offer'].create({
                        'price': self.price,
                        'property_id': property.id,
                        'validity': self.validity,
                        'partner_id': self.partner_id.id,
                    })
                except Exception as e:
                    _logger.error(e)
                    _logger.warning("Cannot make offer for ", property.name)
