from odoo import models, fields, api
from odoo import Command


class EstateProperty(models.Model):
    _inherit = "estate.property"

    invoice_ids = fields.One2many("account.move", "property_id")
    invoice_count = fields.Integer(compute="_compute_invoice_count", string="Total Invoices")

    @api.depends("invoice_ids")
    def _compute_invoice_count(self):
        for record in self:
            record.invoice_count = len(record.invoice_ids)

    def _mark_as_sold(self):
        sold = super()._mark_as_sold()
        for record in self:
            self.env['account.move'].create({
                'partner_id': record.buyer_id.id,
                'move_type': 'out_invoice',
                'property_id': record.id,
                'invoice_line_ids': [
                    Command.create({
                        'name': record.name,
                        'quantity': 1,
                        'price_unit': record.selling_price,
                    }),
                    Command.create({
                        'name': f'Commission (6%) on {record.name}',
                        'quantity': 1,
                        'price_unit': record.selling_price * 0.06,
                    }),
                    Command.create({
                        'name': 'Administrative Fees',
                        'quantity': 1,
                        'price_unit': 100.0,
                    })
                ],
            })
        return sold

    def action_view_invoice(self):
        for record in self:
            invoice = self.env['account.move'].search([('property_id', '=', record.id)], limit=1)
            return {
                'type': 'ir.actions.act_window',
                'name': 'Invoices',
                'res_model': 'account.move',
                'view_mode': 'form',
                'res_id': invoice.id,
            }
