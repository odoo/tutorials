from odoo import api, fields, models

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    sale_order_link_id = fields.Many2one("sale.order.line", ondelete = "cascade")
    sequence= fields.Integer(string = "sequence")
     
    @api.model_create_multi
    def create(self, vals_list):
        lines = super().create(vals_list)

        for line in lines:
            if line.product_template_id.amount > 0:
                deposit_product = self.env['product.template'].search([("id" , "=" , line.product_template_id.id)],limit=1)
                if deposit_product:
                    self.create({
                        "order_id" : line.order_id.id,
                        "product_template_id" : deposit_product.id,
                        "product_uom_qty" : line.product_uom_qty,
                        "price_unit" : line.product_template_id.amount,
                        "sale_order_link_id" : line.id,
                        "name": f"Deposit for {line.name}",
                        "sequence" : line.sequence+1
                    })
        return lines
   
    def write(self , vals):
        res = super().write(vals)

        if "product_uom_qty" in vals:
            for line in self:
                deposit_line = self.search([
                    ('sale_order_link_id', '=' , line.id)
                ])

                if deposit_line:
                    deposit_line.write({
                        "product_uom_qty" : vals["product_uom_qty"],
                        "price_unit" : line.product_template_id.amount
                    })
        return res
