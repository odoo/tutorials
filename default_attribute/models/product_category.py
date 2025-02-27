from odoo import models, fields, api


class ProductCategory(models.Model):
    _inherit = ['product.category']

    show_on_global_info = fields.Boolean(
        string="Show on Global Info",
        help="""For showing this category attributes on global info tab

        Note: You have to add atleast one attribute for showing this category attributes on global info tab"""
    )
    default_attribute_ids = fields.Many2many(
        comodel_name='product.attribute',
        string="Attributes"
    )

    @api.model_create_multi
    def create(self, vals_list):
        categories = super().create(vals_list)
        if any('show_on_global_info' in vals or 'default_attribute_ids' in vals for vals in vals_list):
            categories._update_sale_orders_global_info()

        return categories

    def write(self, vals):
        res = super().write(vals)

        if 'show_on_global_info' in vals or 'default_attribute_ids' in vals:
            self._update_sale_orders_global_info()

        if 'default_attribute_ids' in vals:
            for category in self:
                products = self.env['product.template'].search([('categ_id', '=', category.id)])
                if not products:
                    continue
                else:
                    products._assign_default_attributes()
        return res

    def _update_sale_orders_global_info(self):
        sale_orders = self.env['sale.order'].search([])
        sale_orders._generate_global_info_lines()
