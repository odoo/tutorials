# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, Command, fields, models
from odoo.exceptions import AccessError, UserError


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    invoice_id = fields.Many2one(comodel_name='account.move', string="Invoice", store=True)

    def action_sold(self):
        result = super().action_sold()
        self._create_invoice()
        return result

    def _create_invoice(self):
        invoice_vals = []
        for property in self:
            try:
                property.check_access('write')
            except AccessError:
                raise UserError(_("You do not have permission to change the status of this property."))
            invoice_vals.append({
                'name': _("For selling %s", property.name),
                'move_type': 'out_invoice',
                'partner_id': property.buyer_id.id,
                'estate_property_id': property.id,
                'invoice_line_ids': [
                    Command.create({
                        'name': _("Commission of 6%% for selling property %s", property.name),
                        'quantity': 1,
                        'price_unit': property.selling_price * 0.06,
                    }),
                    Command.create({
                        'name': 'Administrative Fees',
                        'quantity': 1,
                        'price_unit': 100.0,
                    }),
                ]
            })
        invoices = self.env['account.move'].sudo().create(invoice_vals)
        for invoice in invoices:
            invoice.estate_property_id.update({'invoice_id': invoice.id})
        return invoices

    def action_open_invoice(self):
        return {
            'name': _("Open invoice of this estate property"),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_id': 'view_move_form',
            'views': [[False, 'form']],
            'res_model': 'account.move',
            'res_id': self.invoice_id.id,
        }
