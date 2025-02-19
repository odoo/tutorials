# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models
from odoo.exceptions import UserError 


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def sold_action(self):
        for record in self:
            has_access = record.check_access_rights('write', raise_exception=False)
            print(has_access)
            if not has_access:
                raise UserError("You do not have permission to modify properties.")

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
