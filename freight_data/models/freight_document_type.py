from odoo import fields, models


class FreightDocumentType(models.Model):
    _name = "freight.document.type"
    _description = "Freight Document Type Model"
    _inherits = {'freight.data': 'inherit_data'}

    inherit_data = fields.Many2one(
        comodel_name='freight.data',
        ondelete='cascade'
    )
    docs_choice = fields.Selection([
        ('customer_docs', 'Customer Docs'),
        ('operation_docs', 'Operation Docs')
    ], string="Docs Choice")
