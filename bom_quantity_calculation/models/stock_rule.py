from odoo import models, api


class StockRule(models.Model):
    _inherit = ["stock.rule"]

    @api.model
    def _run_buy(self, procurements):
        for procurement, rule in procurements:
            order_name = procurement.origin.split(' - ')[-1]
            source_model = None
            if order_name.startswith("S"):
                source_model = 'sale.order'
            elif order_name.startswith("WH/MO"):
                source_model = 'mrp.production'
            if source_model:
                procurement.values.setdefault(
                    'order_of_work',
                    self.env[source_model].search([('name', '=', order_name)], limit=1).order_of_work
                )
        return super()._run_buy(procurements)

    def _prepare_purchase_order(self, company_id, origins, values):
        purchase_order_vals = super()._prepare_purchase_order(company_id, origins, values)
        purchase_order_vals.update({
            'order_of_work': values[0].get('order_of_work', False)
        })
        return purchase_order_vals

    @api.model
    def _run_manufacture(self, procurements):
        for procurement, rule in procurements:
            order_name = procurement.origin
            source_model = None
            if order_name.startswith("S"):
                source_model = 'sale.order'
            elif order_name.startswith("WH/MO"):
                source_model = 'mrp.production'
            if source_model:
                procurement.values.setdefault(
                    'order_of_work',
                    self.env[source_model].search([('name', '=', order_name)], limit=1).order_of_work
                )
        return super()._run_manufacture(procurements)

    def _prepare_mo_vals(self, product_id, product_qty, product_uom, location_dest_id, name, origin, company_id, values, bom):
        mo_values = super()._prepare_mo_vals(
            product_id, product_qty, product_uom, location_dest_id, name, origin, company_id, values, bom
        )
        mo_values.update({
            'order_of_work': values.get('order_of_work', False)
        })
        return mo_values
