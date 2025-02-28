# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models
from odoo.exceptions import UserError 


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def sold_action(self):
        for record in self:

            self.env['account.move'].sudo().create({
                'partner_id' : record.buyer_id.id,
                'move_type' : 'out_invoice',
                'invoice_line_ids': [
                    (0, 0, {
                        'name': record.name,  
                        'quantity': 1,
                        'price_unit': record.selling_price * 0.06, 
                    }),
                    (0, 0, {
                        'name': 'administrative fees',  
                        'quantity': 1,
                        'price_unit': 100, 
                    })
                ],
            }) 
        return super().sold_action()    
