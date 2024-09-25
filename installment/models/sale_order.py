from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_upload_documents(self):
        """
        This method retrieves required documents based on the configuration settings,
        creates a folder for each sale order if it doesn't exist, and uploads placeholders
        for the required documents in the folder.
        """
        config_settings = self.env["ir.config_parameter"]
        document_settings = {
            "nid": "National ID (NID)",
            "bank_statement": "Bank Statement",
            "rental_contract": "Rental Contract",
            "salary_components": "Salary Components",
            "bank_rate_letter": "Bank Rate Letter",
            "ownership_contract": "Ownership Contract",
        }

        # Get the required documents based on the configuration settings
        required_documents = [
            document_name
            for setting_key, document_name in document_settings.items()
            if config_settings.get_param(f"installment.{setting_key}", default=False)
        ]

        for order in self:
            # Get or create the Installments folder
            installments_folder = self.env["documents.folder"].search(
                [("name", "=", "Installments")], limit=1
            )
            if not installments_folder:
                installments_folder = self.env["documents.folder"].create(
                    {"name": "Installments"}
                )

            # Define folder name based on sale order
            folder_name = order.name.replace("/", "_")
            folder = self.env["documents.folder"].search(
                [
                    ("name", "=", folder_name),
                    ("parent_folder_id", "=", installments_folder.id),
                ],
                limit=1,
            )

            # If folder doesn't exist, create it
            if not folder:
                folder = self.env["documents.folder"].create(
                    {"name": folder_name, "parent_folder_id": installments_folder.id}
                )

            # Create document placeholders for the required documents if they don't exist
            for doc_name in required_documents:
                # Search for document by folder, res_model, and res_id
                existing_doc = self.env["documents.document"].search(
                    [
                        ("folder_id", "=", folder.id),
                        ("res_model", "=", "sale.order"),
                        ("res_id", "=", order.id),
                    ]
                )

                if not existing_doc:
                    self.env["documents.document"].create(
                        {
                            "name": doc_name,
                            "folder_id": folder.id,
                            "partner_id": order.partner_id.id,
                            "res_model": "sale.order",
                            "res_id": order.id,
                            "is_done": False,  # Document not yet uploaded
                        }
                    )

                else:
                    # Check if the document is uploaded, if yes mark it as done
                    if existing_doc.attachment_id:
                        existing_doc.write({"is_done": True})  # Mark as done

        # Return an action to display the documents in the folder
        return {
            "type": "ir.actions.act_window",
            "name": "Documents",
            "res_model": "documents.document",
            "view_mode": "kanban,tree,form",
            "domain": [("folder_id", "=", folder.id)],
            "context": {"searchpanel_default_folder_id": folder.id},
        }


class Document(models.Model):
    _inherit = "documents.document"

    is_done = fields.Boolean(string="Document Uploaded", default=False)

    def write(self, vals):
        """
        Override the write method to mark the document as 'done' when a file is uploaded.
        """
        # Check if the document is getting a file uploaded
        if "attachment_id" in vals:
            # Set is_done to True if the document gets a file
            vals["is_done"] = True

        return super().write(vals)
