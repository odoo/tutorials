from dateutil.relativedelta import relativedelta
import logging
from odoo import fields, models
from odoo.tools.misc import clean_context

_logger = logging.getLogger(__name__)


class DocumentWizard(models.TransientModel):
    _name = "installment.document"

    document_mapping = {
        "installment.nid": "National ID (NID)",
        "installment.salary_components": "Salary Components",
        "installment.bank_statement": "Bank Statement",
        "installment.bank_rate_letter": "Bank Rate Letter",
        "installment.rental_contract": "Rental Contract",
        "installment.ownership_contract": "Ownership Contract",
    }

    name = fields.Char()
    requestee_id = fields.Many2one("res.partner", string="Owner")
    partner_id = fields.Many2one("res.partner", string="Contact")
    activity_note = fields.Html(string="Message")
    activity_date_deadline_range = fields.Integer(string="Due Date In", default=30)
    activity_date_deadline_range_type = fields.Selection(
        [
            ("days", "Days"),
            ("weeks", "Weeks"),
            ("months", "Months"),
        ],
        string="Due type",
        default="days",
    )
    def check_wizard_ok(self):
        # Get the sale order from context
        active_id = self.env.context["active_id"]
        sale_order = self.env["sale.order"].browse(active_id)
        self.partner_id = sale_order.partner_id
        self.name = sale_order.name
        # Calling the method to execute the document upload request process
        self._action_request_upload_documents()

    def _action_request_upload_documents(self):
        workspace_name = "Installment"
        sub_folder = self.name
        existing_workspace = self.env["documents.folder"].search(
            [("name", "=", workspace_name)], limit=1
        )
        if not existing_workspace:
            _logger.info("workspace not exist")
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
            _logger.info("workspace exist")
            existing_sub_folder = self.env["documents.folder"].search(
                [("name", "=", sub_folder)], limit=1
            )
            if not existing_sub_folder:
                _logger.info("sub workspace not exist")
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
                _logger.info("sub workspace exist")
                exiting_doc_list = self.env["documents.document"].search(
                    [("folder_id", "=", existing_sub_folder.id)]
                )
                # Logic for validating docs in sub folder not exist then create
                all_doc = list(self.document_mapping.values())
                for doc in exiting_doc_list:
                    all_doc.remove(doc.name)
                _logger.info("document request:")
                for name in all_doc:
                    self._request_document(name, existing_sub_folder)

    def _get_document_list(self):
        _logger.info("getting the document name from res.config_parameter")
        config_param = self.env["ir.config_parameter"].sudo()
        # Building document required dictionary dynamically
        document = {
            key.split(".")[-1]: name
            for key, name in self.document_mapping.items()
            if config_param.get_param(key, default=False)
        }
        return document

    def _create_document_wizard_request(self, subfolder):
        _logger.info("creating the document request")
        document_required = self._get_document_list()
        for name in document_required.values():
            self._request_document(name, subfolder)

    def _request_document(self, name, subfolder):
        self.ensure_one()
        document = self.env['documents.document'].create({
            'name': name,
            'type': 'empty',
            'folder_id': subfolder.id,
            'owner_id': self.env.user.id,
            'partner_id': self.partner_id.id if self.partner_id else False,
        })

        activity_vals = {
            'user_id': self.requestee_id.user_ids[0].id if self.requestee_id.user_ids else self.env.user.id,
            'note': self.activity_note,
            'summary': name
        }

        deadline = None
        if self.activity_date_deadline_range > 0:
            activity_vals['date_deadline'] = deadline = fields.Date.context_today(self) + relativedelta(
                **{self.activity_date_deadline_range_type: self.activity_date_deadline_range})

        request_by_mail = self.requestee_id and self.create_uid not in self.requestee_id.user_ids
        if request_by_mail:
            share_vals = {
                'name': name,
                'type': 'ids',
                'folder_id': subfolder.id,
                'partner_id': self.partner_id.id if self.partner_id else False,
                'owner_id': self.requestee_id.id,
                'document_ids': [(4, document.id)],
                'activity_note': self.activity_note,
            }
            if deadline:
                share_vals['date_deadline'] = deadline
            share = self.env['documents.share'].create(share_vals)
            share.with_context(clean_context(self.env.context)).send_share_by_mail('documents.mail_template_document_request')
            document.create_share_id = share

        activity = document.with_context(mail_activity_quick_update=request_by_mail).activity_schedule(**activity_vals)
        document.request_activity_id = activity
        return document
