# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, Command, fields, models
from odoo.exceptions import AccessError


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    invoice_id = fields.Many2one(comodel_name='account.move', string="Invoice", store=True)

    def action_sold(self):
        result = super().action_sold()
        if self.env['account.move'].has_access('create'):
            print("Has access rights to billing / invoice.")
        else:
            print("Has no access rights of creating invoice so sudo is required.")
        for property in self:
            try:
                property.check_access('write')
            except AccessError:
                raise AccessError(_("You do not have permission to change the status of this property."))
            invoice = self.env['account.move'].sudo().create({
                'name': f"Invoice for property {property.name}",
                'move_type': 'out_invoice',
                'partner_id': property.buyer_id.id,
                'estate_property_id': property.id,
                'invoice_line_ids': [
                    Command.create({
                        'name': f'Commission of 6% for selling property {property.name}',
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
            property.write({ 'invoice_id': invoice.id })
        return result

    def action_open_invoice(self):
        return {
            'name': _("Open invoice of this estate property"),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_id': 'account_move_invoice_view_form',
            'views': [[False, 'form']],
            'res_model': 'account.move',
            'res_id': self.invoice_id.id,
        }
