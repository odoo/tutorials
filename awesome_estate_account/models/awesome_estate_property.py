from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.fields import Command


class AwesomeEstateProperty(models.Model):
    _inherit = 'awesome.estate.property'

    # -----------------------------------------------------------------------
    # Fields
    # -----------------------------------------------------------------------
    account_move_ids = fields.One2many(
        'account.move',
        'estate_property_id',
        string="Invoices",
    )
    invoice_count = fields.Integer(
        string="Invoice Count",
        compute='_compute_invoice_count',
        help="Number of invoices generated for this property.",
    )

    # -----------------------------------------------------------------------
    # Compute Methods
    # -----------------------------------------------------------------------
    @api.depends('account_move_ids')
    def _compute_invoice_count(self):
        for record in self:
            record.invoice_count = len(record.account_move_ids)

    # -----------------------------------------------------------------------
    # Action Methods
    # -----------------------------------------------------------------------
    def action_sold(self):
        """Mark property as sold, then create a customer invoice."""
        result = super().action_sold()
        self.env['account.move'].create({
            'partner_id': self.buyer_id.id,
            'move_type': 'out_invoice',
            'estate_property_id': self.id,
            'invoice_line_ids': [
                Command.create({
                    'name': _("Commission (6%)"),
                    'quantity': 1,
                    'price_unit': self.selling_price * 0.06,
                }),
                Command.create({
                    'name': _("Administrative Fees"),
                    'quantity': 1,
                    'price_unit': 100.00,
                }),
            ],
        })
        return result

    def action_reset(self):
        """Reset property and cancel all existing invoices."""
        for invoice in self.account_move_ids:
            if invoice.state == 'draft':
                invoice.button_cancel()
            elif invoice.state in ('posted', 'paid'):
                invoice.button_draft()
                invoice.button_cancel()
        return super().action_reset()

    def action_open_invoice(self):
        """Open the invoice for this property."""
        self.ensure_one()
        invoices = self.account_move_ids
        if not invoices:
            raise UserError(_("No invoice found for this property."))
        if len(invoices) == 1:
            return {
                'type': 'ir.actions.act_window',
                'name': _("Invoice"),
                'res_model': 'account.move',
                'res_id': invoices.id,
                'view_mode': 'form',
                'target': 'current',
            }
        return {
            'type': 'ir.actions.act_window',
            'name': _("Invoices"),
            'res_model': 'account.move',
            'domain': [('id', 'in', invoices.ids)],
            'view_mode': 'list,form',
            'target': 'current',
        }
