from odoo import api, fields, models


class ProductSubproductLine(models.Model):
    _name = 'product.subproduct.line'
    _description = "Subproducts"

    product_tmpl_id = fields.Many2one('product.template', ondelete='cascade')
    product_id = fields.Many2one('product.product', string="Product")
    product_uom_qty = fields.Float(related='product_id.qty_available', string="Quantity on Hand")
    kit_unit_qty = fields.Float(string="Kit Unit Qty")
    price_unit = fields.Float(related='product_id.lst_price', string="Unit Price")

    @api.model_create_multi
    def create(self, vals_list):
        lines = super().create(vals_list)
        lines.mapped('product_tmpl_id')._compute_kit_list_price()
        return lines

    def write(self, vals):
        res = super().write(vals)
        self.mapped('product_tmpl_id')._compute_kit_list_price()
        return res

    def unlink(self):
        templates = self.mapped('product_tmpl_id')
        res = super().unlink()
        templates._compute_kit_list_price()
        return res
