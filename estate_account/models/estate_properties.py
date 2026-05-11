import logging

from odoo import api, fields, models
from odoo import Command

_logger = logging.getLogger(__name__)


class EstateProperties(models.BaseModel):
    _inherit = 'estate.properties'

    invoice_count = fields.Integer(compute='_compute_invoice_count')

    def _check_admin_fees(self, admin_fees):
        if admin_fees < 100:
            return 100
        elif admin_fees > 500:
            return 500
        else:
            return admin_fees

    def property_sold(self):
        _logger.error("Reached inherited")
        action = super().property_sold()  # type: ignore
        if self.property_type_id.type == 'Apartment':  # type:ignore
            # _logger.error(self.property_type_id.type)  # type:ignore
            admin_fees = 0.02 * self.selling_price  # type: ignore
            # _logger.error(admin_fees)
            admin_fees = self._check_admin_fees(admin_fees)
            # _logger.error(admin_fees)
        elif self.property_type_id.type == 'House':  # type:ignore
            # _logger.error(self.property_type_id.type)  # type:ignore
            admin_fees = 0.03 * self.selling_price  # type: ignore
            # _logger.error(admin_fees)
            admin_fees = self._check_admin_fees(admin_fees)
            # _logger.error(admin_fees)
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
        # _logger.error(invoice_vals)
        self.env['account.move'].create(invoice_vals)
        return action

    def _find_invoices(self):
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

    @api.depends('state')
    def _compute_invoice_count(self):
        # _logger.error("HELLOOOOOOOOOOO")
        invoices = self._find_invoices()
        for property in self:
            if invoices:
                property.invoice_count = len(invoices)
            else:
                property.invoice_count = 0

    def action_view_partner_invoices(self):
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
