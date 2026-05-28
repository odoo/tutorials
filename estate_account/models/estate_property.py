from odoo import api, fields, models
from odoo import Command


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    invoice_count = fields.Integer(compute='_compute_invoice_count')

    @api.depends('state')
    def _compute_invoice_count(self):
        for record in self:
            invoices = record._find_invoices()
            if invoices:
                record.invoice_count = len(invoices)
            else:
                record.invoice_count = 0

    def _check_admin_fees(self, admin_fees):
        """
        Validates and constrains the administrative fees within a specific range.
        """
        if admin_fees < 100:
            return 100
        elif admin_fees > 500:
            return 500
        else:
            return admin_fees

    def property_sold(self):
        """
        Extends the base property_sold method to generate a customer invoice.

        Calculates administrative fees based on property type (Apartment vs. House)
        and creates an 'account.move' (invoice) with lines for the property
        commission and administrative fees.
        """
        action = super().property_sold()  # type: ignore
        if self.property_type_id.type == 'Apartment':  # type:ignore
            admin_fees = 0.02 * self.selling_price  # type: ignore
            admin_fees = self._check_admin_fees(admin_fees)
        elif self.property_type_id.type == 'House':  # type:ignore
            admin_fees = 0.03 * self.selling_price  # type: ignore
            admin_fees = self._check_admin_fees(admin_fees)
        else:
            admin_fees = 100
        invoice_vals = {
            'move_type': 'out_invoice',
            'partner_id': self.buyer_id.id,  # type: ignore
            'invoice_line_ids': [
                Command.create({
                    'name': f'Property: {self.display_name}',
                    'quantity': 1,
                    'price_unit': 0.06 * self.selling_price,  # type: ignore
                }),
                Command.create({
                    'name': 'Administrative Fees',
                    'quantity': 1,
                    'price_unit': admin_fees
                })
            ]
        }
        self.env['account.move'].create(invoice_vals)
        return action

    def _find_invoices(self):
        """
        Helper method to locate existing customer invoices related to the property.
        """
        self.ensure_one()
        check_name = "Property: " + self.display_name if self.display_name else None
        if check_name and self.selling_price > 0:  # type: ignore
            invoice_lines = self.env['account.move.line'].search([  # type: ignore
                ('move_id.move_type', '=', 'out_invoice'),  # type: ignore
                ('name', 'ilike', check_name),  # type: ignore
            ])
            return invoice_lines.mapped('move_id').ids  # type: ignore
        else:
            return False

    def action_view_partner_invoices(self):
        """
        Returns an action to open the specific invoice associated with the sale.
        """
        if self.selling_price > 0:  # type: ignore
            invoice_ids = self._find_invoices()

            if invoice_ids:
                invoice_ids = int(invoice_ids[0])
                action = self.env["ir.actions.actions"]._for_xml_id("account.action_move_out_invoice")  # type: ignore
                action['res_id'] = invoice_ids
                action['view_mode'] = 'form'
                action['views'] = [(self.env.ref('account.view_move_form').id, 'form')]  # type: ignore
                action['domain'] = [
                    ('id', 'in', invoice_ids),
                    ('partner_id', '=', self.buyer_id.id),  # type: ignore
                ]
                return action
