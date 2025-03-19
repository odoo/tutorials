# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class CatalogCatalog(models.Model):
    _name = 'catalog.catalog'
    _inherit = ['product.catalog.mixin']
    _description = "Catalog Catalog"
     
    name = fields.Char(string="Name")
    date = fields.Date(string="Date", default=lambda self:fields.Date.today())
    catalog_line_ids = fields.One2many(comodel_name='catalog.lines', inverse_name='catalog_line_id')
    company_id = fields.Many2one(
        comodel_name='res.company',
        required=True,
        index=True,
        default=lambda self: self.env.company
    )
    state = fields.Char(default="draft")
    catalog_fields_line_ids = fields.One2many(comodel_name='catalog.fields', inverse_name='catalog_fields_line_id')
    
    def action_open_catalog_view(self):
        return self.with_context(
            order_id=self.id,
            child_field='catalog_line_ids',
            child_ids=self.catalog_line_ids.product_category_id.ids,
            removed_product_ids=self.catalog_line_ids.removed_product_ids.ids
        ).action_add_from_catalog()
    
    def _get_product_catalog_order_line_info(self, product_ids, child_field=False, **kwargs):
        order_line_info = {}
        product_info = self.env['product.product'].search_fetch([],field_names=['list_price', 'type', 'product_tmpl_id'])
        for product in product_info:
            order_line_info[product.id] = {
                'quantity': 0,
                'price': product.list_price,
                'readOnly': False,
                'productType': product.type,
                'product_categ_id': product.product_tmpl_id.categ_id.id
            }    
        return order_line_info
