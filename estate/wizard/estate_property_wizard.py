# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

class EstatePropertyWizard(models.TransientModel):
    _name = 'estate.property.wizard'
    _description = 'Estate Property Wizard'
    
    property = fields.Many2many('estate.property')
    partner_ids = fields.Many2one('res.partner', string='Partners')
