from odoo import api, fields, models


class EstatePropertyOfferWizard(models.TransientModel):
    _name = 'estate.property.offer.wizard'
    _description = 'Make offer'

    price = fields.Float(string="Offer", required=True)
    partner_id = fields.Many2one(comodel_name='res.partner', string="Partner", required=True)
    validity = fields.Integer(string="Validity (Days)", default=7)
