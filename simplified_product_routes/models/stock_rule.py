import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class StockRule(models.Model):
    _inherit = 'stock.rule'
    
    def _get_stock_move_values(self, product_id, product_qty, product_uom, location_id, name, origin, company_id, values):
        """Override to skip rules for invalid configurations"""
        skip_rule = False

        if self.action == 'buy' and not product_id.seller_ids:
            skip_rule = True
            
        if self.action == 'manufacture':
            bom = self.env['mrp.bom']._bom_find(products=product_id, company_id=company_id)
            if not bom:
                skip_rule = True
        
        if skip_rule:
            _logger.info(f"Skipping rule {self.name} for product {product_id.name} due to invalid configuration")
            return False
        
        return super()._get_stock_move_values(
            product_id, product_qty, product_uom, location_id, name, origin, company_id, values
        )
