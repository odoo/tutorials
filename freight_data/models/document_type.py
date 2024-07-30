from odoo import fields, models


class DocumentType(models.Model):
    _name = 'document.type'
    _description = 'Document Type Model'
    _inherits = {'port.city': 'freight_type_id'}

    freight_type_id = fields.Many2one('port.city')
    doc_type = fields.Selection(
        [('customer_docs', 'Customer Docs'), ('operation_docs', 'Operation Docs')],
        string="Type",
        required=True
    )