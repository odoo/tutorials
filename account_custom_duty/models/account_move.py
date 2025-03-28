from odoo import _, fields, models
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = "account.move"

    account_journal_entry_custom_duty = fields.Many2one(
        "account.move", readonly=True
    )
    account_custom_currency_rate = fields.Monetary(
        string="Custom Currency Rate",
        currency_field="currency_id",
    )
    account_bill_reference = fields.Char(string="Bill Reference")
    account_bill_entry_number = fields.Char(string="Bill of Entry Number")
    account_bill_entry_date = fields.Date(string="Bill of Entry Date")
    account_port_code = fields.Char(string="Port Code")
    custom_duty_line_ids = fields.One2many("account.move.custom.duty.line", "move_id", string="Custom Duty Lines")

    def action_account_custom_duty_wizard(self):
        """
        Opens the "Custom Duty Entry" wizard for the current journal entry.

        - Ensures the record is in the "posted" state.
        - Ensures the GST treatment is one of the following:
            - Overseas
            - Special Economic Zone (SEZ)
            - Deemed Export
        - Opens the "Custom Duty Entry" wizard as a modal.

        Returns:
            dict: An `ir.actions.act_window` dictionary to open the wizard.

        Raises:
            UserError: If the move is not posted or the GST treatment is invalid.
        """
        self.ensure_one()
        if self.state != "posted" or self.l10n_in_gst_treatment not in [
            "overseas",
            "special_economic_zone",
            "deemed_export"
        ]:
            raise UserError(_("This action can only be performed on posted moves with overseas, special economic zone, or deemed export GST treatment."))
        return {
            "name": _("Custom Duty Entry"),
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "account.custom.duty.wizard",
            "view_id": self.env.ref("account_custom_duty.bill_entry_wizard_view_form").id,
            "target": "new",
            "context": {
                "move_id": self.id
            },
        }

    def action_account_bill_of_entry(self):
        """
        Opens the "Bill of Entry" form for the custom duty journal entry.

        - Ensures a related journal entry exists for the custom duty.
        - Opens the existing `account.move` record associated with the bill of entry.

        Returns:
            dict: An `ir.actions.act_window` dictionary to open the bill of entry.

        Raises:
            UserError: If no custom duty journal entry is linked to the move.
        """
        self.ensure_one()
        if not self.account_journal_entry_custom_duty:
            raise UserError(_("No custom duty entry found for this move."))
        return {
            "name": _("Bill of Entry"),
            "type": "ir.actions.act_window",
            "res_model": "account.move",
            "view_mode": "form",
            "view_id": self.env.ref("account.view_move_form").id,
            "res_id": self.account_journal_entry_custom_duty.id,
        }
