from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.fields import Command


class AwesomeEstateProperty(models.Model):
    """Add accounting integration to the estate property model.

    This inheritance adds:
    - A One2many link to invoices generated from this property
    - A computed invoice count field for stat buttons
    - An action method to open the related invoice
    """
    _inherit = 'awesome.estate.property'

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
    # Computed Fields
    # -----------------------------------------------------------------------
    @api.depends('account_move_ids')
    def _compute_invoice_count(self):
        for record in self:
            record.invoice_count = len(record.account_move_ids)

    # -----------------------------------------------------------------------
    # Action Methods
    # -----------------------------------------------------------------------
    def action_open_invoice(self):
        """Open the invoice for this property.

        If exactly one invoice exists, it opens that invoice's form view.
        If multiple invoices exist (e.g., from repeated sales), it opens
        a filtered list view.
        """
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

    def action_sold(self):
        """Mark property as sold, then create a customer invoice.

        Calls the original ``action_sold()`` first to perform the state
        transition and all validations.  After the property is confirmed
        as sold, an ``account.move`` (out_invoice) is created with two
        lines: a 6% commission on the selling price and a flat $100
        administrative fee.

        The generated invoice is linked back to the property via the
        ``estate_property_id`` field for bidirectional navigation.
        """
        # Step 1 — let the base module handle the state transition.
        result = super().action_sold()

        # Step 2 — build and create the customer invoice.
        self.env['account.move'].create({
            'partner_id': self.buyer_id.id,
            'move_type': 'out_invoice',
            'estate_property_id': self.id,
            'invoice_line_ids': [
                Command.create({
                    'name': _("Commission (6%%)"),
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
