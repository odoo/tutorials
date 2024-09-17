from odoo import models


class SalesOrder(models.Model):
    _name = "sale.order"
    _inherit = "sale.order"

    def action_upload_documents(self):
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "documents.document_action"
        )
        return action
