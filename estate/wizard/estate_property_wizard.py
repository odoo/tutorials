# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

class EstatePropertyWizard(models.TransientModel):
    _name = 'estate.property.wizard'
    _description = 'Estate Property Wizard'
    
    property_ids = fields.Many2many('estate.property')
    price=fields.Float(string="Price")
    validity=fields.Integer(string="Validity")
    partner_id = fields.Many2one('res.partner', string='Partners')

    def add_offer(self):
        for property in self.property_ids:
            self.env['estate.property.offer'].create({
                'price': self.price,
                'validity': self.validity,
                'property_id': property.id,
                'partner_id': self.partner_id.id,
            })
