# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, models
from odoo.exceptions import UserError

class CatalogProductTemplateReport(models.AbstractModel):
    _name = 'report.catalog.catalog_product_template_report'
    _description = 'Catalog Product Template Report'

    def _get_report_values(self, docids, data):
        catalog = self.env['catalog.catalog'].browse(docids)
        catalog_fields = catalog.catalog_fields_line_ids.sorted(lambda f: f.sequence).mapped('fields')
        remove_ids = catalog.catalog_line_ids.removed_product_ids.ids
 
        if len(catalog_fields) == 0:
            raise UserError(_("Please add field names inside the Fields page in the catalog."))
        if len(catalog.catalog_line_ids) == 0:
            raise UserError(_("Please select a category before proceeding."))
            
        catalog_fields += ['categ_id', 'id']
        catalog_line_color = {
            catalog_line['product_category_id'].id: [
                catalog_line['color1'],
                catalog_line['color2']
            ]
            for catalog_line in catalog.catalog_line_ids
        }
        catalog_info = {
            category.id: {
                'products': [],
                'color': [],
                'category_name': category.name
            }
            for category in catalog.catalog_line_ids.product_category_id
        }
        category_id = catalog.catalog_line_ids.product_category_id.ids

        for product_info in self.env['product.product'].search_read([('categ_id', 'in', category_id)], fields=catalog_fields):
            category_id = product_info['categ_id'][0]
            catalog_info[category_id]['products'].append(product_info)
            color1 = catalog_line_color[category_id][0]
            color2 = catalog_line_color[category_id][1]

            if len(catalog_info[category_id]['color']) < 2:
                catalog_info[category_id]['color'].append(color1)
                catalog_info[category_id]['color'].append(color2)
 
        catalog_info['remove_ids'] = remove_ids
        docs = [{
            'catalog_info':catalog_info,
            'category_ids': catalog.catalog_line_ids.product_category_id.ids,
            'fields_order': catalog_fields,
            'remove_ids':remove_ids
        }]
        return {
            'docs': docs
        }
