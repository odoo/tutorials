from odoo import api, fields, models

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    primary_warehouse_id = fields.Many2one('stock.warehouse', string='Primary Warehouse', required=True, default=lambda self: self._default_primary_warehouse())
    secondary_warehouse_id = fields.Many2one('stock.warehouse', string='Secondary Warehouse')

    @api.model
    def _default_primary_warehouse(self):
        """Fetch the default primary warehouse (e.g., the first available one)."""
        return self.env['stock.warehouse'].search([], limit=1).id
