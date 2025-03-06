from odoo import fields, models
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    zero_stock_approval = fields.Boolean(string="Approval", help="Administrator approval is required for zero stock products.")



    def fields_get(self, allfields=None, attributes=None):
        """
        Dynamically modify field attributes based on user groups.
        """

        # Get the all fields of model
        fields_metadata = super().fields_get(allfields, attributes)

        if "zero_stock_approval" in fields_metadata:

            # If the user is a Administrator, then the field is editable otherwise, for any other user it is read-only.
            if self.env.user.has_group("sales_team.group_sale_manager"):
                fields_metadata["zero_stock_approval"]["readonly"] = False
            else:
                fields_metadata["zero_stock_approval"]["readonly"] = True

        return fields_metadata


    def action_confirm(self):
        """
        Override the Sale Order confirmation action to enforce Zero Stock Approval validation.
        """

        for line in self.order_line:
            # Less than or equal to zero product quantity for approval is required
            if line.product_uom_qty <= 0 and self.zero_stock_approval == False:
                raise ValidationError("You cannot confirm this Sale Order without Zero Stock Approval.")

        return super().action_confirm()
