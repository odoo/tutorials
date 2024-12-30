from odoo import api, Command, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    is_warranty_in_order_line = fields.Boolean(default=False)
    related_warranty_line_id = fields.Many2one(
        comodel_name="sale.order.line", ondelete="cascade"
    )

    @api.model
    def unlink(self):
        for line in self:
            # Check if this line is a warranty line
            if line.related_warranty_line_id:
                # Reset the fields on the related main product line
                related_line = line.related_warranty_line_id
                related_line.is_warranty_in_order_line = False
        return super(SaleOrderLine, self).unlink()


class SaleOrder(models.Model):
    _inherit = "sale.order"

    has_warranty_product_in_order = fields.Boolean(
        compute="_compute_has_warranty_product_in_sale_order"
    )

    @api.depends("order_line")
    def _compute_has_warranty_product_in_sale_order(self):
        for order in self:
            order.has_warranty_product_in_order = any(
                (line.product_id.has_warranty and not line.is_warranty_in_order_line)
                for line in order.order_line
            )

    def action_get_product_ids_with_warranty_from_order_line(self):
        active_order_line = [
            line
            for line in self.order_line
            if line.product_id.has_warranty and not line.is_warranty_in_order_line
        ]

        warranty_lines = {
            "warranty_line_ids": [
                Command.create({"product_id": line.product_id.id})
                for line in active_order_line
            ]
        }
        warranty_wizard = self.env["warranty.wizard"].create(warranty_lines)

        return {
            "type": "ir.actions.act_window",
            "name": "Warranty Wizard",
            "res_model": "warranty.wizard",
            "res_id": warranty_wizard.id,
            "view_mode": "form",
            "target": "new",
        }
