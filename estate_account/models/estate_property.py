from odoo import models, fields
from odoo.exceptions import AccessError, UserError
from odoo.tools import groupby


class Property(models.Model):
    _inherit = "estate.property"

    # invoice_count = fields.Integer(string='Invoice Count', compute='_get_invoiced', readonly=True)
    invoice_line_id = fields.Many2one('account.move.line', string='Invoice Line', readonly=True, copy=False)
    invoice_id = fields.Many2one("account.move", string='Invoices', related='invoice_line_id.move_id',
                                 readonly=True,
                                 copy=False)

    # invoice_status = fields.Selection([
    #    ('upselling', 'Upselling Opportunity'),
    #    ('invoiced', 'Fully Invoiced'),
    #    ('to invoice', 'To Invoice'),
    #    ('no', 'Nothing to Invoice')
    # ], string='Invoice Status', compute='_get_invoice_status', store=True, readonly=True)

    def action_sold(self):
        res = super().action_sold()
        self._create_invoices()
        return res

    def _get_invoice_grouping_keys(self):
        return ['partner_id']

    def _prepare_invoice(self):
        self.ensure_one()

        values = {
            'ref': '',
            'move_type': 'out_invoice',
            'partner_id': self.buyer_id.id,
            'invoice_line_ids': [],
            'user_id': self.salesperson_id.id,
            'invoice_origin': self.name
        }

        return values

    def _prepare_invoice_line(self, sequence=0):
        """Prepare the values to create the new invoice line for a sales order line.

        :param optional_values: any parameter that should be added to the returned invoice line
        :rtype: dict
        """
        self.ensure_one()

        res = {
            'display_type': 'product',
            'sequence': sequence,
            'name': self.env['account.move.line']._get_journal_items_full_name(self.name, 'House Sale'),
            'quantity': 1,
            'price_unit': self.selling_price,
            'property_ids': [fields.Command.link(self.id)],
        }

        return res

    # trying to understand sales invoice creation line by line
    def _create_invoices(self, grouped=False, date=None):
        if not self.env['account.move'].has_access('create'):
            try:
                self.check_access('write')
            except AccessError:
                return self.env['account.move']

        invoice_vals_list = []
        for invoice_item_sequence, record in enumerate(self):
            if record.state != 'sold':
                raise UserError('You can only invoice sold properties.')

            if record.buyer_id.lang:
                record = record.with_context(lang=record.buyer_id.lang)

            invoice_vals = record._prepare_invoice()
            invoice_vals['invoice_line_ids'].append(
                fields.Command.create(record._prepare_invoice_line(sequence=invoice_item_sequence))
            )
            invoice_vals_list.append(invoice_vals)

        if not grouped:
            new_invoice_vals_list = []
            invoice_grouping_keys = self._get_invoice_grouping_keys()
            invoice_vals_list = sorted(
                invoice_vals_list,
                key=lambda x: [
                    x.get(grouping_key) for grouping_key in invoice_grouping_keys
                ]
            )

            for _grouping_keys, invoices in groupby(invoice_vals_list,
                                                    key=lambda x: (x.get(grouping_key) for grouping_key in
                                                                   invoice_grouping_keys)):
                origins = set()
                refs = set()
                ref_invoice_vals = None
                for invoice_vals in invoices:
                    if not ref_invoice_vals:
                        ref_invoice_vals = invoice_vals
                    else:
                        ref_invoice_vals['invoice_line_ids'] += invoice_vals['invoice_line_ids']
                    origins.add(invoice_vals['invoice_origin'])
                    refs.add(invoice_vals['ref'])

                ref_invoice_vals.update({
                    'ref': ', '.join(refs)[:2000],
                    'invoice_origin': ', '.join(origins)
                })
                new_invoice_vals_list.append(ref_invoice_vals)
            invoice_vals_list = new_invoice_vals_list

            return self.env['account.move'].sudo().with_context(default_move_type='out_invoice').create(
                invoice_vals_list)

    def action_view_invoice(self):
        action = self.env['ir.actions.actions']._for_xml_id('account.action_move_out_invoice_type')
        form_view = [(self.env.ref('account.view_move_form').id, 'form')]
        if 'views' in action:
            action['views'] = form_view + [(state, view) for state, view in action['views'] if view != 'form']
        else:
            action['views'] = form_view
        action['res_id'] = self.invoice_id.id

        return action
