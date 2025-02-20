# -- coding: utf-8 --
# Part of Odoo. See LICENSE file for full copyright and licensing details.  

from odoo import models, fields, api

class EstatePropertyOfferWizard(models.TransientModel):
    _name = 'estate.property.offer.wizard'
    _description = 'Property Offer Wizard'

    property_id = fields.Many2one('estate.property', string="Property", required=True)
    partner_id = fields.Many2one('res.partner', string="Buyer", required=True)
    price = fields.Float(string="Offer Price", required=True)

    def action_create_offer(self):
        self.env['estate.property.offer'].create({
            'property_id': self.property_id.id,
            'partner_id': self.partner_id.id,
            'price': self.price,
        })
