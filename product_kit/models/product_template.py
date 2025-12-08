from odoo import api, fields, models
from odoo.exceptions import UserError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_kit = fields.Boolean(string="Is Kit")
    sub_products = fields.Many2many(comodel_name='product.product', string='Sub Products')

    @api.onchange('sub_products')
    def _onchange_sub_products(self):
        for product in self:
            sub_product_tmp_ids = self.sub_products.mapped('product_tmpl_id')
            if product._origin.id in sub_product_tmp_ids.ids:
                raise UserError('You can not add product itself as a sub-product')
