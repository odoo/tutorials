# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, Command, fields, models
from odoo.exceptions import AccessError


class EstateProperty(models.Model):
    _inherit = "estate.property"

    invoice_id = fields.Many2one("account.move", string="Invoice", store=True)

    def action_sold(self):
        try:
            self.check_access("write")
        except AccessError:
            raise AccessError(_("You do not have permission to change the status of this property."))
        
        if self.env['account.move'].has_access('create'):
            print(_("Has access rights to billing / invoice"))
        else:
            print(_("Has no access rights to creating invoice so sudo is required"))

        for property in self:
            invoice = self.env["account.move"].sudo().create({
                "name": f"Invoice for property {property.name}",
                "estate_property_id": property.id,
                "move_type": "out_invoice",
                "partner_id": property.buyer_id.id,
                "invoice_line_ids": [
                    Command.create({
                        "name": f"Commission of 6% for selling property {property.name}",
                        "quantity": 1,
                        "price_unit": property.selling_price * 0.06,
                    }),
                    Command.create({
                        "name": "Administrative Fees",
                        "quantity": 1,
                        "price_unit": 100.0,
                    }),
                ]
            })
            property.write({ "invoice_id": invoice.id })
        return super().action_sold()

    def action_open_invoice(self):
        return {
            'name': _('Open invoice of this estate property'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_id': 'account_move_invoice_view_form',
            'views': [[False, 'form']],
            'res_model': 'account.move',
            'res_id': self.invoice_id.id,
        }
