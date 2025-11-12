import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)

class EstateWizardMultiOffer(models.TransientModel):
    _name = "estate.wizard.multi.offer"
    _description = "Add Offer Wizard"

    price = fields.Float(string="Offer Price", required=True)
    validity = fields.Integer(string="Validity (days)", default=7, required=True)
    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)


    def action_make_offer(self):
        for property in self.env.context.get('active_ids'):
            try:
                self.env["estate.property.offer"].create({
                    "partner_id": self.partner_id.id,
                    "price": self.price,
                    "validity": self.validity,
                    'property_id': property
                })
            except Exception as e:
                _logger.warning("Offers can only be created for properties with 'New' or 'Offer Received' status!"
                                
)
