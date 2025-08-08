from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    warranty_end_date = fields.Date("Warranty End Date")
    is_warranty_line = fields.Boolean(compute="_compute_is_warranty_line", store=True)

    @api.depends('warranty_end_date', 'product_id.product_tmpl_id.has_warranty')
    def _compute_is_warranty_line(self):
        for line in self:
            line.is_warranty_line = bool(line.warranty_end_date and line.product_id.product_tmpl_id.has_warranty)

    def unlink(self):
        for line in self:
            if not line.is_warranty_line:
                product_template = line.product_id.product_tmpl_id
                warranty_lines = self.env['sale.order.line'].search([
                    ('order_id', '=', line.order_id.id),
                    ('product_id.product_tmpl_id', '=', product_template.id),
                    ('warranty_end_date', '!=', False),
                    ('is_warranty_line', '=', True),
                ])
                if warranty_lines:
                    warranty_lines.unlink()
        return super(SaleOrderLine, self).unlink()
