from odoo import models, fields


class DocumentType(models.Model):
    _name = 'document.type'
    _description = 'Document Type'

    name = fields.Char(string='Name', required=True)
    doc_type = fields.Selection([
        ('customer', 'Customer Docs'),
        ('operation', 'Operation Docs'),
    ], string='Document Type', required=True)
    status = fields.Boolean(string='Status', default=True)
