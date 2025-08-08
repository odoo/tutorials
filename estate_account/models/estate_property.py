# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import Command, models, _
from odoo.exceptions import UserError

class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        for record in self:
            # has_access = record.check_access_rights('write', raise_exception=False)
            # print(has_access)
            # if not has_access:
            #     raise UserError(_("You do not have permission to modify properties."))

            try:
                record.check_access('write')
                has_access = True
            except AccessError:
                has_access = False

            print(has_access)
            if not has_access:
                raise UserError(_("You do not have permission to modify properties."))

            invoice_vals = {
                "partner_id" : record.buyer_id.id,
                "move_type" : "out_invoice",
                "invoice_line_ids" : [
                    Command.create({
                        "name" : f"Commission (6%) on {record.name}",
                        "quantity" : 1,
                        "price_unit" : record.selling_price * 0.06
                    }),
                    Command.create({
                        "name" : "Administrative Fees",
                        "quantity" : 1,
                        "price_unit" : 100
                    }),
                ]
            }
            print(" reached ".center(100, '='))
            invoice = record.env["account.move"].sudo().create(invoice_vals)
        return super().action_sold()
