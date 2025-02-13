# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, Command

class EstateProperty(models.Model):
    _inherit="estate.property"
    
    def action_sold(self):
        # breakpoint()
        self.env["account.move"].create({
            "partner_id":self.partner_id.id,
            "move_type": "out_invoice",
            "invoice_line_ids":[
                Command.create(
                    {
                        "name":self.name,
                        "quantity":1,
                        "price_unit":self.selling_price 
                    }
                ),
                Command.create(
                    {
                        "name":"tax 6%",
                        "quantity":1,
                        "price_unit":self.selling_price * 0.06 
                    }
                ),
                Command.create(
                    {
                        "name": "administrative fees",
                        "quantity": 1,
                        "price_unit": 100.00 
                    }
                ),
            ]
        })
        return super().action_sold()
