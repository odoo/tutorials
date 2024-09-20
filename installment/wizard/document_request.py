from odoo import models, fields
from odoo.exceptions import ValidationError
from odoo.tools.misc import clean_context
from dateutil.relativedelta import relativedelta


class documentsRequest(models.TransientModel):
    _name = "documents.request"

    name = fields.Char(string="Document Name")
    requestee_id = fields.Many2one("res.partner", string="Owner")
    partner_id = fields.Many2one("res.partner", string="Contact")

    activity_type_id = fields.Many2one(
        "mail.activity.type",
        string="Activity type",
    )

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

    def filling_wizard(self):
        active_id = self.env.context.get("active_id")
        sale_order = self.env["sale.order"].browse(active_id)
        self.partner_id = sale_order.partner_id.id
        self.name = sale_order.name
        self.action_upload_documents_from_sale_order()

    def action_upload_documents_from_sale_order(self):

        active_id = self.env.context.get("active_id")
        sale_order = self.env["sale.order"].browse(active_id)

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

        folder = f"Sales Order {sale_order.name.replace('/', '')}"
        subfolder = self.env["documents.folder"].search([("name", "=", folder)])

        if not subfolder:
            subfolder = self.env["documents.folder"].create(
                {
                    "name": folder,
                    "parent_folder_id": installment_folder.id,
                    "has_write_access": True,
                }
            )
        if not subfolder:
            raise ValidationError(
                "Failed to create or find the corresponding subfolder."
            )

        settings = self.env["ir.config_parameter"].sudo()
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
                document_data = {
                    "name": f"{doc_type}",
                    "folder_id": subfolder.id,
                }

                self.request_document(doc_type, subfolder)

    def request_document(self, name, sub_folder):
        self.ensure_one()
        document = self.env["documents.document"].create(
            {
                "name": name,
                "type": "empty",
                "folder_id": sub_folder.id,
                "owner_id": self.env.user.id,
                "partner_id": self.partner_id.id if self.partner_id else False,
            }
        )

        activity_vals = {
            "user_id": (
                self.requestee_id.user_ids[0].id
                if self.requestee_id.user_ids
                else self.env.user.id
            ),
            "note": self.activity_note,
            "activity_type_id": (
                self.activity_type_id.id if self.activity_type_id else False
            ),
            "summary": name,
        }

        deadline = None
        if self.activity_date_deadline_range > 0:
            activity_vals["date_deadline"] = deadline = fields.Date.context_today(
                self
            ) + relativedelta(
                **{
                    self.activity_date_deadline_range_type: self.activity_date_deadline_range
                }
            )

        request_by_mail = (
            self.requestee_id and self.create_uid not in self.requestee_id.user_ids
        )
        if request_by_mail:
            share_vals = {
                "name": name,
                "type": "ids",
                "folder_id": sub_folder.id,
                "partner_id": self.partner_id.id if self.partner_id else False,
                "owner_id": self.requestee_id.id,
                "document_ids": [(4, document.id)],
                "activity_note": self.activity_note,
            }
            if deadline:
                share_vals["date_deadline"] = deadline

            share = self.env["documents.share"].create(share_vals)
            share.with_context(clean_context(self.env.context)).send_share_by_mail(
                "documents.mail_template_document_request"
            )
            document.create_share_id = share

        activity = document.with_context(
            mail_activity_quick_update=request_by_mail
        ).activity_schedule(**activity_vals)
        document.request_activity_id = activity
        return document
