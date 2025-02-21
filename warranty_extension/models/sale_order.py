from odoo import models, fields, api

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



class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    is_warranty = fields.Boolean(string="Is Warranty", default=False)

    @api.model_create_multi
    def create(self, vals_list):
        """Ensure warranty lines are marked accordingly on creation."""
        for vals in vals_list:
            if vals.get("is_warranty") and "product_id" in vals:
                product = self.env["product.template"].browse(vals["product_id"])
                if product:
                    vals["name"] = f"Warranty for {product.name}"
        return super().create(vals_list)

    def unlink(self):
        """Remove associated warranty lines when the main product is deleted."""
        lines_to_delete = self.env['sale.order.line']
        
        for line in self:
            # If this is a warranty line (has 'Valid until' in name), just add it
            if "Valid until" in (line.name or ''):
                lines_to_delete |= line
                continue
                
            # For product lines, find and delete their warranty lines
            warranty_lines = line.order_id.order_line.filtered(
                lambda l: f"For product: {line.product_id.name}" in (l.name or '') 
                and f"Valid until" in (l.name or '')
            )
            if warranty_lines:
                print(f"Found {len(warranty_lines)} warranty lines for product {line.product_id.name}")
                lines_to_delete |= warranty_lines
            
            # Add the product line itself
            lines_to_delete |= line
        
        return super(SaleOrderLine, lines_to_delete).unlink()
