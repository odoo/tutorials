from odoo import api, fields, models


class ProductKitWizard(models.TransientModel):
    _name = "product.kit.wizard"
    _description = "Sub Product Kit Wizard"

    main_product_id = fields.Many2one(
        'product.product',
        string="Product",
    )
    sale_line_id = fields.Many2one('sale.order.line')
    line_ids = fields.One2many(
        'product.wizard.kit.line',
        'wizard_id',
        string="Sub Product"
    )

    @api.model
    def _default_get(self, fields_list):
        res = super().default_get(fields_list)

        sale_line = self.env['sale.order.line'].browse(
            self.env.context.get('active_id')
        )
        if not sale_line.product_id:
            return res
        order = sale_line.order_id
        product = sale_line.product_id
        lines = []

        for sub_product in product.product_tmpl_id.sub_product:
            existing_line = order.order_line.filtered(
                lambda l:
                l.product_id == sub_product
                and l.kit_parent_line_id == sale_line
            )[:1]

            lines.append(
                (0, 0, {
                    "product_id": sub_product.id,
                    "quantity": (
                        existing_line.product_uom_qty
                        if existing_line else 1.0
                    ),
                    "price": (
                        existing_line.extra_price
                        if existing_line else sub_product.lst_price
                    ),
                })
            )

        res.update({
            "sale_line_id": sale_line.id,
            "main_product_id": product.id,
            "line_ids": lines,
        })

        return res
