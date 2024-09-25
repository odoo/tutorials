from odoo import models
from odoo.exceptions import ValidationError


class sale_order(models.Model):
    _inherit = "sale.order"

    def action_upload_documents_from_sale_order(self):
        installment_folder = self.env["documents.folder"].search(
            [("name", "=", "Installment Documents")], limit=1
        )

        if not installment_folder:

            installment_folder = self.env["documents.folder"].create(
                {
                    "name": "Installment Documents",
                    "parent_folder_id": None,
                    "has_write_access": True,
                }
            )

        subfolder = self.env["documents.folder"].search([("name", "=", self.name)])
        if not subfolder:
            subfolder = self.env["documents.folder"].create(
                {
                    "name": self.name,
                    "parent_folder_id": installment_folder.id,
                    "has_write_access": True,
                }
            )
        if not subfolder:
            raise ValidationError(
                "Failed to create or find the corresponding subfolder."
            )

        settings = self.env["ir.config_parameter"]
        nid = settings.get_param("installment.nid") == "True"
        salary_components = (
            settings.get_param("installment.salary_components") == "True"
        )
        bank_statement = settings.get_param("installment.bank_statement") == "True"
        bank_rate_letter = settings.get_param("installment.bank_rate_letter") == "True"
        rental_contract = settings.get_param("installment.rental_contract") == "True"
        ownership_contract = (
            settings.get_param("installment.owership_contract") == "True"
        )

        documents_to_upload = {
            "Rental Contract": rental_contract,
            "Bank Rate Letter": bank_rate_letter,
            "Bank Statement": bank_statement,
            "Salary Components": salary_components,
            "NID": nid,
            "Owership Contract": ownership_contract,
        }

        for doc_type, should_upload in documents_to_upload.items():
            if should_upload:
                # Check if the document already exists in the subfolder
                existing_document = self.env["documents.document"].search(
                    [
                        ("                       ", "=", doc_type),
                        ("folder_id", "=", subfolder.id),
                    ],
                    limit=1,
                )

                # Create the document only if it does not already exist
                if not existing_document:
                    document_data = {
                        "name": f"{doc_type}",
                        "folder_id": subfolder.id,
                    }
                    self.env["documents.document"].create(document_data)
        return {
            "type": "ir.actions.act_window",
            "name": "Documents",
            "res_model": "documents.document",
            "view_mode": "kanban,tree,form",
            "domain": [("folder_id", "=", subfolder.id)],
            "context": {"searchpanel_default_folder_id": subfolder.id},
        }
