from odoo import api, fields, models


class Picking(models.Model):
    _inherit = 'stock.picking'

    sale_ids = fields.Many2many(
        "sale.order",
        "picking_sale_order_rel", 
        "picking_id",
        "sale_id",  
    )

    purchase_ids = fields.Many2many(
        "purchase.order",
        "picking_purchase_order_rel", 
        "picking_id",
        "purchase_id",  
    )

    new_return_ids = fields.Many2many(
        "stock.picking", 
        "picking_new_return_rel",
        "picking_id",
        "return_id",
    )
