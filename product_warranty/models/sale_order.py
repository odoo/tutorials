from odoo import api, models, fields


class SaleOrder(models.Model):
    _inherit = "sale.order"

    show_warranty_button = fields.Boolean(compute='_compute_show_warranty_button')
    def action_open_custom_warranty_wizard(self):
        self.ensure_one()
        return {
            "name": "Add Warranty",
            "type": "ir.actions.act_window",
            "res_model": "add.warranty.wizard",
            "view_mode": "form",
            "target": "new",
        }

    @api.depends("order_line.product_id")
    def _compute_show_warranty_button(self):
        for record in self:
            record.show_warranty_button = any(line.product_template_id.is_warranty for line in record.order_line)
