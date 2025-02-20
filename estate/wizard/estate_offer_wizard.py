# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class EstateOfferWizard(models.Model):
    _name = "estate.offer.wizard"
    _description = "Estate Offer Wizard"

    price = fields.Float(string="Price", required=True)
    partner_id = fields.Many2one('res.partner', string="Buyer", required=True)
    property_ids = fields.Many2many(
        'estate.property', string="Properties", domain=[("state", "in", ["new", "offer_received"])])

    def action_make_offer(self):
        offer = self.env['estate.property.offer']
        for property in self.property_ids:
            offer.create({
                'price': self.price,
                'partner_id': self.partner_id.id,
                'property_id': property.id
            })
        return {'type': 'ir.actions.act_window_close'}
