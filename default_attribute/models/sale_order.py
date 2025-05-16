from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    global_info_line_ids = fields.One2many(
        comodel_name='global.info.line',
        inverse_name='order_id',
        string="Global Info Lines",
    )

    product_category_id = fields.Integer(
        related='global_info_line_ids.product_category_id.id',
        string="Product Category",
    )

    @api.model_create_multi
    def create(self, vals_list):
        orders = super(SaleOrder, self).create(vals_list)
        orders._generate_global_info_lines()
        return orders

    def _generate_global_info_lines(self):
        for order in self:
            product_categories = self.env['product.category'].search([('show_on_global_info', '=', True)])
            existing_lines = { (line.product_category_id.id, line.attribute_id.id): line.id for line in order.global_info_line_ids }

            new_global_info_list = []
            keep_line_ids = set()

            for category in product_categories:
                for attribute in category.default_attribute_ids:
                    key = (category.id, attribute.id)
                    if key in existing_lines:
                        keep_line_ids.add(existing_lines[key])
                    else:
                        new_global_info_list.append({
                            'order_id': order.id,
                            'product_category_id': category.id,
                            'attribute_id': attribute.id,
                        })

            unlink_line_ids = set(existing_lines.values()) - keep_line_ids
            if unlink_line_ids:
                self.env['global.info.line'].browse(list(unlink_line_ids)).unlink()

            if new_global_info_list:
                self.env['global.info.line'].create(new_global_info_list)
