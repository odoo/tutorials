from odoo import models, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.model_create_multi
    def create(self, vals_list):
        rec = super().create(vals_list)
        for vals in vals_list:
            if vals.get('is_rental'):
                deposite_product = self.env.company.product_deposit
                product_template = self.env['product.template'].browse(vals.get('product_template_id'))
                if product_template.required_deposit and deposite_product:
                    deposite_number = vals.get('product_uom_qty')
                    if deposite_product.id == vals.get('product_id'):
                        self.create({
                            'order_id': vals['order_id'],
                            'product_id': deposite_product.id,
                            'product_uom_qty': deposite_number,
                            'price_unit': product_template.amount_deposit * deposite_number,
                            'name': 'Deposit Amount',
                        })
        return rec
