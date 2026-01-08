from odoo import api, fields, models

class SaleOrderLine(models.Model):
    _inherit="sale.order.line"

    divided_amount_ids = fields.Many2many("sale.order.line.division.tag", string="Division")
    divided_from_line_id = fields.Many2one("sale.order.line", string="Divided From")

    def action_open_distriute_wizard(self):
        self.ensure_one()
        return {
            'name': "Distribute",
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order.distribute',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'current_order_id': self.order_id.id,
                'current_order_line_id': self.id
            },
        }

    @api.ondelete(at_uninstall=False)
    def _unlink_restore_original_price(self):
        for line in self:
            if line.divided_amount_ids:
                line.divided_from_line_id.price_subtotal += line.divided_amount_ids.name
                if line.divided_from_line_id.product_uom_qty:
                    line.divided_from_line_id.price_unit = line.divided_from_line_id.price_subtotal / line.divided_from_line_id.product_uom_qty
