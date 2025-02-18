# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class EstatePropertyOfferWizard(models.TransientModel):
    _name = 'estate.property.offer.wizard'

    price = fields.Float(string='Price')
    validity = fields.Integer(string='Validity (days)', default=7)

    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_ids = fields.Many2many('estate.property', string='Properties')

    def add_offer(self):
        for property in self.property_ids:
            self.env['estate.property.offer'].create({
                'price': self.price,
                'validity': self.validity,
                'property_id': property.id,
                'partner_id': self.partner_id.id,
            })
        return { 'type': 'ir.actions.act_window_close' }
