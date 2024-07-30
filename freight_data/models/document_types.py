from odoo import models, fields


class DocumentTypes(models.Model):
    _name = "document.types"
    _description = "Document Types"

    name = fields.Char(string='Name', required=True)
    status = fields.Boolean(string='Status', default=True)
    doc_type = fields.Selection([
        ('customer_docs', 'Customer Docs'),
        ('operation_docs', 'Operation Docs')
    ], string='Document Type', required=True, default='customer_docs')
