from odoo import api, models


class SaleOrderLine(models.Model):
    _inherit = ['sale.order.line']

    @api.ondelete(at_uninstall=True)
    def _onDelete_sale_order_line(self):
        self._update_global_discount('delete')

    def _get_global_discount_id(self):
        return int(self.extra_tax_data.get(
            "computation_key").split(",")[1])

    def _update_global_discount(self, operation):
        for record in self:
            discount_order_line = record.order_id.order_line.filtered(
                lambda o: o._is_global_discount())
            if discount_order_line and record.id not in discount_order_line.ids:
                for val in discount_order_line:
                    DOL_id = val._get_global_discount_id()
                    domain = [('order_id', 'in', record.order_id),
                              ('id', 'not in', discount_order_line.ids)]
                    if operation == 'delete':
                        domain.append(('id', 'not in', record.ids))
                    total_price = dict(record.env['sale.order.line']._read_group(
                        domain=domain, aggregates=['price_subtotal:sum'], groupby=['order_id'])).get(record.order_id, 0.0)
                    if total_price == 0:
                        val.unlink()
                        continue
                    discount_per = record.env['sale.order.discount'].search(
                        domain=[('sale_order_id', 'in', record.order_id), ('id', '=', DOL_id)]).discount_percentage
                    new_price = -(total_price * discount_per)
                    val.update({
                        'price_unit': new_price})

    def write(self, vals):
        res = super().write(vals)
        self._update_global_discount('update')
        return res
