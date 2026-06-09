from odoo import api, Command, fields, models


class SubKitProductWizard(models.TransientModel):
    _name = "sale.kit.product.sub.product.wizard"
    _description = "Sub products view of a kit product"

    sale_line_id = fields.Many2one("sale.order.line")
    wizard_line_ids = fields.One2many(
        "sale.kit.product.wizard.line", "product_wizard_line"
    )

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        active_id = self.env.context.get("active_id")
        res["sale_line_id"] = self.env["sale.order.line"].browse(active_id)
        sub_product_ids = res["sale_line_id"].product_id.product_tmpl_id.sub_products
        if sub_product_ids:
            lines = []
            for sub_product in sub_product_ids:
                lines.append(
                    Command.create(
                        {
                            "product_id": sub_product.id,
                            "product_qty": 1,
                            "product_price": sub_product.lst_price,
                        }
                    )
                )
            # res["wizard_line_ids"] = lines
            res.update({"wizard_line_ids": lines})

        return res
