# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    invoice_count = fields.Integer(compute='_compute_invoice_count', string='Invoice Count')

    def _compute_invoice_count(self):
        for property_record in self:
            property_record.invoice_count = self.env['account.move'].search_count([
                ('estate_property_id', 'in', property_record.ids),
                ('move_type', '=', 'out_invoice'),
            ])

    def action_view_invoices(self):
        self.ensure_one()
        invoices = self.env['account.move'].search([
            ('estate_property_id', '=', self.id),
            ('move_type', '=', 'out_invoice'),
        ])
        action = self.env.ref('account.action_move_out_invoice_type').read()[0]
        action['domain'] = [
            ('estate_property_id', '=', self.id),
            ('move_type', '=', 'out_invoice'),
        ]
        action['context'] = {
            'default_move_type': 'out_invoice',
            'default_partner_id': self.buyer_id.id,
            'default_estate_property_id': self.id,
        }
        if len(invoices) == 1:
            form_view = [(self.env.ref('account.view_move_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state, view) for state, view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = invoices.id
        return action

    def action_sold(self):

        self.env['account.move'].create({
            'partner_id': self.buyer_id.id,
            'move_type': 'out_invoice',
            'estate_property_id': self.id,
            'journal_id': self.env['account.journal'].search([('type', '=', 'sale')], limit=1).id,
            'line_ids': [
                # 6% of the selling price
                (0, 0, {
                    'name': self.name,
                    'quantity': 1,
                    'price_unit': self.selling_price * 0.06,
                }),
                # 100.00 from administrative fees
                (0, 0, {
                    'name': 'Administrative Fees',
                    'quantity': 1,
                    'price_unit': 100.00,
                }),

            ],
        })

        return super().action_sold()


class AccountMove(models.Model):
    _inherit = 'account.move'

    estate_property_id = fields.Many2one('estate.property', string='Property')
