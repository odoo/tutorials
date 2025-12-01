# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.http import Controller, request, route
from odoo import Command


class CatalogProductConfiguratorController(Controller):
    @route(route='/catalog/product_configurator/update_catalog_line_info', type='json', auth='user')
    def catalog_product_configurator_update_catalog_line_info(self, catalog_id, category_id, checkbox_checked, removed_product_ids):
        catalog = request.env['catalog.catalog'].browse(catalog_id)
        product_ids = request.env['product.product'].search([('categ_id', '=', category_id)]).ids
        if checkbox_checked:
            request.env['catalog.lines'].sudo().create({
                'catalog_line_id': catalog_id,
                'product_category_id': category_id,
                'removed_product_ids': [Command.link(id) for id in removed_product_ids if id in product_ids]
            })
        else:
            delete_command = [
                Command.delete(catalog_line.id)
                for catalog_line in catalog.catalog_line_ids
                if(catalog_line.product_category_id.id == category_id)
            ]
            catalog.catalog_line_ids = delete_command
        return

    @route(route='/catalog/product_configurator/update_catalog_line_info/using_record', type='json', auth='user')
    def catalog_product_configurator_update_catalog_line_info_using_record(self, catalog_id, category_id, product_id, is_add):
        catalog = request.env['catalog.catalog'].browse(catalog_id)
        if is_add:
            line = [line for line in catalog.catalog_line_ids if line.product_category_id.id == category_id]
            line[0].removed_product_ids = [Command.unlink(product_id)]
        else:
            if category_id in catalog.catalog_line_ids.product_category_id.ids:
               line = catalog.catalog_line_ids.filtered(lambda line: line.product_category_id.id == category_id)
               line.removed_product_ids = [Command.link(product_id)]
            else:
                request.env['catalog.lines'].sudo().create({
                'catalog_line_id': catalog_id,
                'product_category_id': category_id,
                'removed_product_ids': [Command.link(product_id)]
            })
        return
