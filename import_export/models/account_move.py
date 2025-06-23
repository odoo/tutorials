from odoo import api, fields, models
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = "account.move"

    # Track which invoice generated the custom duty journal entry
    import_export_journal_entry_id = fields.Many2one(
        "account.move",
        string="Import Duty Journal Entry",
        readonly=True,
        help="Journal entry created for import duties and taxes",
    )
    is_bill_of_entry_eligible = fields.Boolean(
        string="Is Eligible for Bill of Entry",
        compute="_compute_is_bill_of_entry_eligible",
        help="Whether this invoice is eligible for import duty processing",
    )

    @api.depends("state", "l10n_in_gst_treatment", "move_type")
    def _compute_is_bill_of_entry_eligible(self):
        """Determine if an invoice is eligible for import duty processing

        An invoice is eligible when:
        1. It has been posted
        2. It has appropriate GST treatment (overseas/SEZ/deemed export)
        3. It's a vendor bill (in_invoice)
        """
        for move in self:
            move.is_bill_of_entry_eligible = (
                move.state == "posted"
                and move.l10n_in_gst_treatment
                in ["overseas", "special_economic_zone", "deemed_export"]
                and move.move_type == "in_invoice"
            )

    def action_open_import_export_wizard(self):
        """Open the import duty wizard for eligible invoices"""
        self.ensure_one()
        # No need to check eligibility as the button will be invisible if not eligible
        # This is just an extra validation
        if not self.is_bill_of_entry_eligible:
            raise UserError(
                "This invoice is not eligible for import duty processing. "
                "Ensure it is posted and has the correct GST treatment (overseas/SEZ/deemed export).",
            )

        return {
            "name": "Import Duty Entry",
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "import.export.wizard",
            "view_id": self.env.ref("import_export.import_export_wizard_view_form").id,
            "target": "new",
            "context": {"move_id": self.id},
        }
