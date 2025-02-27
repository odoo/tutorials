from odoo import models,fields,api

class SaleOrderLine(models.Model):
    _inherit= "sale.order.line"

    is_kit_product = fields.Boolean(string="Is Kit Product", compute="_compute_is_kit", store=True)

    @api.depends("product_id")
    def _compute_is_kit(self):
        for line in self:
            line.is_kit_product = line.product_id.product_tmpl_id.is_kit 

    def action_open_kit_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Kit Wizard',
            'res_model': 'kit.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context' : {'active_id':self.id}
        }
