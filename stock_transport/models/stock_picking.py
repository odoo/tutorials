from odoo import models,fields,api

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    weight = fields.Float()
    volume = fields.Float()