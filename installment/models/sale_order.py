from odoo import models


class SalesOrder(models.Model):
    _inherit = "sale.order"

    def document_upload(self):
        workspace_name = "Installment"
        sub_folder = self.name
        documents = {
            'name': 'Documents',
            'type': 'ir.actions.act_window',
            'res_model': 'documents.document',
            'view_mode': 'kanban,tree,form',
        }

        # Search for existing workspace folder
        existing_workspace = self.env["documents.folder"].search(
            [("name", "=", workspace_name)], limit=1
        )

        # Create workspace folder if it doesn't exist
        if not existing_workspace:
            existing_workspace = self.env["documents.folder"].create({
                "name": workspace_name,
                "parent_folder_id": None,
                "description": f"Workspace for {workspace_name}",
                "has_write_access": True,
            })

        # Search for existing subfolder within the workspace
        existing_sub_folder = self.env["documents.folder"].search(
            [("name", "=", sub_folder), ("parent_folder_id", "=", existing_workspace.id)], limit=1
        )

        # Create subfolder if it doesn't exist
        if not existing_sub_folder:
            existing_sub_folder = self.env["documents.folder"].create({
                "name": sub_folder,
                "parent_folder_id": existing_workspace.id,
                "description": f"Subfolder for {sub_folder} under {workspace_name}",
                "has_write_access": True,
            })
            for name in self._get_document_list():
                self._request_document(name, existing_sub_folder)
        else:
            # Fetch existing documents in the subfolder
            exiting_doc_list = self.env["documents.document"].search(
                [("folder_id", "=", existing_sub_folder.id)]
            )

            # Get the list of documents that need to be created
            all_doc = self._get_document_list()
            for doc in exiting_doc_list:
                if doc.name in all_doc:
                    all_doc.remove(doc.name)

            # Request documents if they don't exist
            for name in all_doc:
                self._request_document(name, existing_sub_folder)

        documents['domain'] = [('folder_id', '=', existing_sub_folder.id)]
        documents['context'] = {'searchpanel_default_folder_id': existing_sub_folder.id}

        return documents

    def _get_document_list(self):
        # Fetching configuration parameters
        config_param = self.env["ir.config_parameter"]

        # Initialize the list to store required documents
        document_list = []

        # Check each config parameter and add the corresponding document name if enabled
        if config_param.get_param("installment.nid", default=False):
            document_list.append("National ID (NID)")
        if config_param.get_param("installment.salary_components", default=False):
            document_list.append("Salary Components")
        if config_param.get_param("installment.bank_statement", default=False):
            document_list.append("Bank Statement")
        if config_param.get_param("installment.bank_rate_letter", default=False):
            document_list.append("Bank Rate Letter")
        if config_param.get_param("installment.rental_contract", default=False):
            document_list.append("Rental Contract")
        if config_param.get_param("installment.ownership_contract", default=False):
            document_list.append("Ownership Contract")

        return document_list

    def _request_document(self, name, subfolder):

        document = self.env['documents.document'].create({
            'name': name,
            'type': 'empty',
            'folder_id': subfolder.id,
            'owner_id': self.env.user.id,
            'partner_id': self.partner_id.id if self.partner_id else False,
        })

        return document
