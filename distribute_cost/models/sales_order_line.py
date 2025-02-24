from odoo import fields, models,api

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def action_distribute_cost(self):
        print("========== Action Distribute Cost Called ==========")
        return {
            'type': 'ir.actions.act_window',
            'name': 'Distribute Cost',
            'res_model': 'distribute.cost.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_order_id': self.id},
        }