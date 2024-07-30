from odoo import api, fields, models

class CustomsExportDescription(models.Model):
    _name = 'customs.export.description'
    _description = 'Customs Expert Description Model'

    commodity_data_id = fields.Many2one('commodity.data')
    description = fields.Char(string="Description")
    
