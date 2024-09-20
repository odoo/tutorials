from odoo import models


class SaleOrder(models.Model):
    _name = "sale.order"
    _inherit = "sale.order"

    def action_upload_documents(self):

        config_settings = self.env["ir.config_parameter"].sudo()

        document_settings = {
            "nid": "National ID (NID)",
            "bank_statement": "Bank Statement",
            "rental_contract": "Rental Contract",
            "salary_components": "Salary Components",
            "bank_rate_letter": "Bank Rate Letter",
            "ownership_contract": "Ownership Contract",
        }

        required_documents = []
        for setting_key, document_name in document_settings.items():
            if config_settings.get_param(f"installment.{setting_key}", default=False):
                required_documents.append(document_name)

        for order in self:

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

                    self.env["documents.document"].create(
                        {
                            "name": doc_name,
                            "folder_id": folder.id,
                            "partner_id": order.partner_id.id,
                            "res_model": "sale.order",
                            "res_id": order.id,
                        }
                    )

        return {
            "name": "Documents",
            "type": "ir.actions.act_window",
            "res_model": "documents.document",
            "view_mode": "kanban,tree,form",
            "domain": [("folder_id", "=", folder.id)],
        }
