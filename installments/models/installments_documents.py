from odoo import models


class InstallmentsDocuments(models.Model):
    _inherit = 'sale.order'

    def create_sale_order_folder(self):
        """
        This method is responsible for creating or retrieving the Installments folder and
        the specific folder for the sale order. It returns the folder where documents
        will be uploaded.
        """
        # Get or create the Installments parent folder
        installments_folder = self.env["documents.folder"].search(
            [("name", "=", "Installments")], limit=1
        )
        if not installments_folder:
            installments_folder = self.env["documents.folder"].create(
                {"name": "Installments"}
            )
        # Define the folder name based on sale order
        folder_name = self.name.replace("/", "_")
        # Check if a folder for the current sale order exists
        folder = self.env["documents.folder"].search(
            [
                ("name", "=", folder_name),
                ("parent_folder_id", "=", installments_folder.id),
            ],
            limit=1,
        )
        # If the folder doesn't exist, create it
        if not folder:
            folder = self.env["documents.folder"].create(
                {"name": folder_name, "parent_folder_id": installments_folder.id}
            )
        return folder

    def action_upload_documents(self):
        """
        This method retrieves required documents based on the configuration settings,
        and uploads placeholders for the required documents in the folder created for the sale order.
        """
        config_settings = self.env["ir.config_parameter"]
        document_settings = {
            "nid": "National ID (NID)",
            "bank_statement": "Bank Statement",
            "rental_contract": "Rental Contract",
            "salary_components": "Salary Components",
            "bank_rate_letter": "Bank Rate Letter",
            "owernship_contract": "Ownership Contract",
        }
        # Get the required documents based on the configuration settings
        required_documents = [
            document_name
            for setting_key, document_name in document_settings.items()
            if config_settings.get_param(f"installments.{setting_key}", default=False)
        ]
        for order in self:
            # Call the function to create or get the folder for the sale order
            folder = order.create_sale_order_folder()
            # Create document placeholders for the required documents if they don't exist
            for doc_name in required_documents:
                existing_doc = self.env["documents.document"].search(
                    [
                        ("folder_id", "=", folder.id),
                        ("name", "=", doc_name),
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
                        }
                    )
        # Return an action to display the documents in the folder
        return {
            "type": "ir.actions.act_window",
            "name": "Documents",
            "res_model": "documents.document",
            "view_mode": "kanban,tree,form",
            "domain": [("folder_id", "=", folder.id)],
            "context": {"folder_id": folder.id},
        }
