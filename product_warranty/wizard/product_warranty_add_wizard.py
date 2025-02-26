from odoo import api, Command, fields, models

class AddWarranty(models.TransientModel):
    _name = "product.warranty.add.wizard"
    _description = "Add Warranty To Order Lines"

    line_ids = fields.One2many(
        "product.warranty.wizard.line", "wizard_id" 
    )

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list) or {} 
        active_id = self.env.context.get("active_id")
        if active_id:
            sale_order = self.env["sale.order"].browse(active_id)
            if sale_order.exists():
                warranty_lines = []
                for line in sale_order.order_line:
                    if line.linked_line_ids:
                        warranty_lines.append(
                            Command.create({
                                "sale_order_line_id": line.id,
                                "warranty_config_id": line.linked_line_ids[0].warranty_id,
                            })
                        )
                    elif line.product_template_id and line.product_template_id.is_warranty:
                        warranty_lines.append(
                            Command.create({
                                "sale_order_line_id": line.id,
                                "warranty_config_id": False,
                            })
                        )
                res["line_ids"] = warranty_lines
        return res

    def add_warranty(self):
        sale_order_id = self.env.context.get("active_id")
        for line in self.line_ids:
            sale_order_line = line.sale_order_line_id
            if line.warranty_config_id:
                warranty = line.warranty_config_id
                product_template_id = warranty.product_template_id
                price = (warranty.percentage / 100) * sale_order_line.price_subtotal
                linked_line_id = sale_order_line.id
                name = (
                    "Extended Warranty of %.1f Years - %s (Ends on %s)"
                    % (
                        warranty.years,
                        product_template_id.display_name,
                        line.date_end,
                    )
                )
                # Check if a warranty line already exists for the linked line and warranty
                existing_warranty_line = self.env["sale.order.line"].search([
                    ("linked_line_id", "=", linked_line_id),
                ], limit=1)
                if existing_warranty_line:
                    existing_warranty_line.write({
                        "name": name,
                        "price_unit": price,
                        "product_id": product_template_id.product_variant_id.id,
                        "warranty_id": warranty.id,
                    })
                else:
                    self.env["sale.order.line"].create({
                        "order_id": sale_order_id,
                        "name": name,
                        "product_id": product_template_id.product_variant_id.id,
                        "product_uom_qty": sale_order_line.product_uom_qty,
                        "linked_line_id": linked_line_id,
                        "price_unit": price,
                        "warranty_id": warranty.id,
                    })
            #remove the applied warranty        
            else:
                if sale_order_line.linked_line_ids:
                    sale_order_line.linked_line_ids[0].unlink()

        return {"type": "ir.actions.act_window_close"}
        