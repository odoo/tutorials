from odoo import fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    modular_type_id = fields.Many2one("modular.type", string="Module Type")
