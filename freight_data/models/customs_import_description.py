from odoo import api, fields, models

class CustomsImportDescription(models.Model):
    _name = 'customs.import.description'
    _description = 'Customs Import Description Model'

    commodity_data_id = fields.Many2one('commodity.data')
    description = fields.Char(string="Description")