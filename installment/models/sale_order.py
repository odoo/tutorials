from odoo import models


class SalesOrder(models.Model):
    _inherit = "sale.order"

    document_mapping = {
        "installment.nid": "National ID (NID)",
        "installment.salary_components": "Salary Components",
        "installment.bank_statement": "Bank Statement",
        "installment.bank_rate_letter": "Bank Rate Letter",
        "installment.rental_contract": "Rental Contract",
        "installment.ownership_contract": "Ownership Contract",
    }

    def action_upload_documents(self):
        workspace_name = "Installment"
        sub_folder = self.name
        existing_workspace = self.env["documents.folder"].search(
            [("name", "=", workspace_name)], limit=1
        )
        if not existing_workspace:
            new_workspace = self.env["documents.folder"].create(
                {
                    "name": workspace_name,
                    "parent_folder_id": None,
                    "description": f"Workspace for {workspace_name}",
                    "has_write_access": True,
                }
            )
            subfolder = self.env["documents.folder"].create(
                {
                    "name": sub_folder,
                    "parent_folder_id": new_workspace.id,
                    "description": f"Subfolder for {sub_folder} under {workspace_name}",
                    "has_write_access": True,
                }
            )
            self._create_document_wizard_request(subfolder)

        else:
            existing_sub_folder = self.env["documents.folder"].search(
                [("name", "=", sub_folder)], limit=1
            )
            if not existing_sub_folder:
                subfolder = self.env["documents.folder"].create(
                    {
                        "name": sub_folder,
                        "parent_folder_id": existing_workspace.id,
                        "description": f"Subfolder for {sub_folder} under {workspace_name}",
                        "has_write_access": True,
                    }
                )
                self._create_document_wizard_request(subfolder)
            else:
                exiting_doc_list = self.env["documents.document"].search(
                    [("folder_id", "=", existing_sub_folder.id)]
                )
                # Logic for validating docs in sub folder not exist then create
                unmatched_doc = []
                for doc in exiting_doc_list:
                    if doc.name not in self.document_mapping.values():
                        unmatched_doc.append(doc.name)
                for name in unmatched_doc:
                    values = {
                        "name": name,
                        "owner_id": self.env.user.id,
                        "partner_id": self.partner_id.id,
                        "folder_id": subfolder.id,
                    }
                    self.env["documents.document"].create(values)

    def _get_document_list(self):
        config_param = self.env["ir.config_parameter"].sudo()
        # Building document required dictionary dynamically
        document = {
            key.split(".")[-1]: name
            for key, name in self.document_mapping.items()
            if config_param.get_param(key, default=False)
        }
        return document

    def _create_document_wizard_request(self, subfolder):
        document_required = self._get_document_list()
        for name in document_required.values():
            values = {
                "name": name,
                "owner_id": self.env.user.id,
                "partner_id": self.partner_id.id,
                "folder_id": subfolder.id,
            }
            self.env["documents.document"].create(values)
