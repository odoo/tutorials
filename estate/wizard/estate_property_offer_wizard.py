# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class EstatePropertyOfferWizard(models.Model):
    _name = 'estate.property.offer.wizard'
    _description = 'Wizard to add offers to multiple properties'

    price = fields.Float(string='Offer Price', required=True)
    validity = fields.Integer(string='Offer Validity (days)', required=True, default=7)
    buyer_id = fields.Many2one('res.partner', string='Buyer', required=True)
    property_ids = fields.Many2many('estate.property', string='Properties')

    def action_make_offer(self):
        for prop in self.property_ids:
            self.env['estate.property.offer'].create({
                'property_id': prop.id,
                'price': self.price,
                'validity': self.validity,
                'partner_id': self.buyer_id.id,
            })
        return {'type': 'ir.actions.act_window_close'}
