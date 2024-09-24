from odoo import api, fields, models

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    warranty_product_id = fields.Integer("Attached Product Id")

    # @api.ondelete(at_uninstall=False)
    # def _delete_recode_with_warranty(self):
    #     print("Executed the delition of warranty along with product.")
    #     product_id = None

    #     for record in self:
    #         product_id = record.id
    #         warranty = self.env['sale.order.line'].search([("warranty_product_id", "=", product_id)])
    #         warranty.unlink()
    #         print(warranty.id)
    #         print("Executed the delition of warranty along with product.", product_id)

    def unlink(self):
        for line in self:
            # Check if any other order lines have this line as their warranty product
            warranty_lines = self.search([('warranty_product_id', '=', line.id)])
            if warranty_lines:
                # If warranty lines exist, delete them
                warranty_lines.unlink()
        
        # Call super to delete the original order lines (including the product being removed)
        return super(SaleOrderLine, self).unlink()