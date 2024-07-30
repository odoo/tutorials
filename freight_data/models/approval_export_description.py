from odoo import fields, models


class ApprovalExportDescription(models.Model):
    _name = 'approval.export.description'
    _description = 'Approval Export Description Model'

    commodity_data_id = fields.Many2one('commodity.data')
    description = fields.Char(string="Description")
