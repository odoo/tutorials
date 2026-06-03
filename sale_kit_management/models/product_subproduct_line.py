from odoo import api, fields, models


class ProductSubproductLine(models.Model):
    _name = 'product.subproduct.line'
    _description = "Subproducts"

    product_tmpl_id = fields.Many2one('product.template', ondelete='cascade')
    product_id = fields.Many2one('product.product', string="Product", required=True)
    product_uom_qty = fields.Float(related='product_id.qty_available', string="Quantity on Hand")
    kit_unit_qty = fields.Float(string="Kit Unit Qty", default=1.0)
    price_unit = fields.Float(string="Unit Price", compute='_compute_price_unit', store=True, readonly=False)

    @api.depends('product_id')
    def _compute_price_unit(self):
        for line in self:
            if line.product_id:
                line.price_unit = line.product_id.lst_price
            else:
                line.price_unit = 0.0

    @api.model_create_multi
    def create(self, vals_list):
        lines = super().create(vals_list)
        lines.mapped('product_tmpl_id')._recompute_kit_list_price()
        return lines

    def write(self, vals):
        res = super().write(vals)
        if 'price_unit' in vals or 'kit_unit_qty' in vals or 'product_id' in vals:
            self.mapped('product_tmpl_id')._recompute_kit_list_price()
        return res

    def unlink(self):
        templates = self.mapped('product_tmpl_id')
        res = super().unlink()
        templates._recompute_kit_list_price()
        return res
