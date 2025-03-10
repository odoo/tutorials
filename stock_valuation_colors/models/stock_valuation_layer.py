from odoo import api, fields, models


class StockValuationLayer(models.Model):
    _inherit = "stock.valuation.layer"

    is_scrap = fields.Boolean(related='stock_move_id.scrapped')
    code = fields.Selection(related='stock_move_id.picking_code', store=True)
    is_inventory = fields.Boolean(related='stock_move_id.is_inventory')
