from odoo import Command, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    has_kit = fields.Boolean(related="product_template_id.kit", store=True, help="Check product has kit enable or not")
    is_kit = fields.Boolean(string="Is kit", default=False, help="Distinguish main product and subproduct. If true it is sub product")

    def open_kit_wizard(self):
        for record in self:
            sale_order_line_id = record.id
            sale_order_id = record.order_id.id

            existing_lines = []

            # Fetching existing order lines from sale order
            existing_lines = self.env['sale.order.line'].search([
                ('linked_line_id', '=', sale_order_line_id),
                ('order_id', '=', sale_order_id)
            ])

            # Creating dictionary with product id as key and quantity as value from existing order line
            existing_dict = {
                line.product_id.id: line.product_uom_qty for line in existing_lines
            }
            product_commands = []

            # Looping through all the subproduct of kit enabled product
            for product in record.product_template_id.subproduct:
                qty = existing_dict.get(product.id, 1)  # Fetching quantity of product if not found return 1
                # Creating command to create new linked record
                product_commands.append(
                    Command.create({
                        "product_id": product.id,
                        "quantity": qty
                    })
                )

            # Populating wizard models
            wizard = self.env['wizard.product.kit'].create({
                "product_ids": product_commands
            })

            return {
                'type': 'ir.actions.act_window',
                'name': 'Product Kit',
                'res_model': 'wizard.product.kit',
                'view_mode': 'form',
                'target': 'new',
                "res_id": wizard.id,
                "context": {
                    "default_sale_order_id": record.order_id.id,
                }
            }
