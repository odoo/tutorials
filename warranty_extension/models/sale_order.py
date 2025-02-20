from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_warranty_selection_wizard(self):
        self.ensure_one()
        action = self.env["ir.actions.act_window"]._for_xml_id("warranty_extension.action_warranty_selection_wizard")
        warranty_line_ids = []

        # Only process products that have warranties available
        for line in self.order_line.filtered(lambda l: l.product_id.product_tmpl_id.warranty_configuration_ids):
            product_tmpl = line.product_id.product_tmpl_id
            print(f"Processing product {product_tmpl.name} with {len(product_tmpl.warranty_configuration_ids)} warranties")
            
            for warranty in product_tmpl.warranty_configuration_ids:
                print(f"Adding warranty option: {warranty.name} for product {product_tmpl.name}")
                warranty_line_ids.append((0, 0, {
                    'product_id': product_tmpl.id,
                    'warranty_id': warranty.id,
                    'end_date': fields.Date.add(fields.Date.today(), years=warranty.year),
                    'selected': False
                }))

        if not warranty_line_ids:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'No Warranties Available',
                    'message': 'None of the products in this order have warranties available.',
                    'type': 'warning',
                    'sticky': False,
                }
            }

        action['context'] = {
            'default_sale_order_id': self.id,
            'default_warranty_lines': warranty_line_ids,
        }

        return action
