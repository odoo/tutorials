from odoo import api, models, fields, Command
from datetime import timedelta


class InvoiceCreate(models.Model):
    _inherit = "sale.order"

    # create cron function
    @api.model
    def action_cron_auto_transfer(self):
        invoices = self.env["account.move "].search(
            [
                (
                    "line_ids.product_id",
                    "=",
                    self.env.ref("installment.product1").id,
                ),
                ("state", "in", ["posted", "open"]),
                ("payment_state", "!=", "paid"),
                ("penalty_applied", "=", False),
            ]
        )

        current_date = fields.Date.today()
        for invoice in invoices:
            penalty_delay_date = self.env["ir.config_parameter"].get_param(
                "installment.delay_panalty_process"
            )

            penalty_delay_days = int(float(penalty_delay_date))
            invoice_date = invoice.invoice_date_due + timedelta(days=penalty_delay_days)

            if current_date >= invoice_date:
                penalty_amount = self.calculate_penalty_amount(invoice)
                values = {
                    "move_type": "out_invoice",
                    "partner_id": invoice.partner_id.id,
                    "invoice_date": fields.Date.today(),
                    "penalty_applied": True,
                    "invoice_line_ids": [
                        Command.create(
                            {
                                "name": "Installment included total amount",
                                "product_id": self.env.ref("installment.product1").id,
                                "price_unit": invoice.amount_total,
                                "quantity": 1.0,
                                "tax_ids": None,
                            }
                        ),
                        Command.create(
                            {
                                "name": "Penalty amount.",
                                "product_id": self.env.ref("installment.product3").id,
                                "price_unit": penalty_amount,
                                "quantity": 1.0,
                                "tax_ids": None,
                            }
                        ),
                    ],
                }
                new_invoice = self.env["account.move"].create(values)
                new_invoice.action_post()

    # calculate penalty amounte
    def calculate_penalty_amount(self, invoice):
        down_penalty_percentage = float(
            self.env["ir.config_parameter"].get_param("installment.delay_panalty_perc")
        )

        penalty_invoice_amount = (invoice.amount_total * down_penalty_percentage) / 100
        return penalty_invoice_amount

    # create fuction for document upload
    def action_upload_documents(self):
        # Retrieve the configuration settings
        config_settings = self.env["ir.config_parameter"]

        # Create a mapping of setting fields to document names
        document_settings = {
            "nid": "National ID (NID)",
            "bank_statement": "Bank Statement",
            "rental_contract": "Rental Contract",
            "salary_component": "Salary Components",
            "bank_rate_letter": "Bank Rate Letter",
            "owner_contract": "Ownership Contract",
        }

        # Prepare a list of required docu   ents based on the configuration
        required_documents = []
        for setting_key, document_name in document_settings.items():
            if config_settings.get_param(f"installment.{setting_key}", default=False):
                required_documents.append(document_name)
        for order in self:
            # Ensure the Installments folder exists
            installments_folder = self.env["documents.folder"].search(
                [("name", "=", "Installments")], limit=1
            )
            if not installments_folder:
                installments_folder = self.env["documents.folder"].create(
                    {
                        "name": "Installments",
                        "parent_folder_id": None,
                    }
                )

            # Create the sales order folder inside the Installments folder
            folder_name = f"{order.name.replace('/', '_')}"
            folder = self.env["documents.folder"].search(
                [
                    ("name", "=", folder_name),
                    ("parent_folder_id", "=", installments_folder.id),
                ],
                limit=1,
            )

            if not folder:
                folder = self.env["documents.folder"].create(
                    {
                        "name": folder_name,
                        "parent_folder_id": installments_folder.id,
                    }
                )

            # Create the document requests (placeholders) in the folder
            for doc_name in required_documents:
                # Check if the document already exists as a placeholder
                existing_doc = self.env["documents.document"].search(
                    [
                        ("folder_id", "=", folder.id),
                        ("name", "=", doc_name),
                        ("res_model", "=", "sale.order"),
                        ("res_id", "=", order.id),
                    ],
                )

                if not existing_doc:
                    # Create a new placeholder document
                    self.env["documents.document"].create(
                        {
                            "name": doc_name,
                            "folder_id": folder.id,
                            "partner_id": order.partner_id.id,
                            "res_model": "sale.order",
                            "res_id": order.id,
                        }
                    )

        # Open the folder in the Documents app
        return {
            "name": "Documents",
            "type": "ir.actions.act_window",
            "res_model": "documents.document",
            "view_mode": "kanban,tree,form",
            "domain": [("folder_id", "=", folder.id)],
            "context": {
                "searchpanel_default_folder_id": folder.id,
                "searchpanel_default_partner_id": order.partner_id.id,
            },
        }
