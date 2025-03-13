from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError

class SaleOrder(models.Model):
    _inherit = "sale.order"

    approval_id = fields.Many2one(
        "approval.category",
        string="Approval Type",
        compute="_compute_approval_type",
        readonly=True,
        store=True
    )
    show_approval_type = fields.Boolean(
        string="Show Approval Type"
    )
    approval_request_id = fields.Many2one(
        "approval.request",
        string="Approval Request"
    )
    approval_status = fields.Selection(
        related="approval_request_id.request_status",
        string="Approval Status",
        store=True
    )
    needs_approval = fields.Boolean(
        string="Needs Approval",
        default=True
    )

    def _get_approval_type(self, amount):
        """
            Fetch the correct approval category based on the order amount.
        """
        return self.env["approval.category"].search(
            [
                ("is_sales_approval", "=", True),
                ("from_amount", "<=", amount),
                "|", ("to_amount", "=", False),
                ("to_amount", ">=", amount)
            ],
            order="to_amount desc", limit=1
        )

    @api.depends("amount_total")
    def _compute_approval_type(self):
        """
            Compute and assign the correct approval type based on amount.
        """
        for order in self:
            order.approval_id = self._get_approval_type(order.amount_total).id

        self.needs_approval = True

    def action_sent_for_approval(self):
        """
            Send sale order for approval, ensuring correct approval type is assigned.
        """
        for order in self:
            if not order.order_line:
                raise ValidationError("You cannot send an empty order for approval. Please add at least one product.")
            
            approval_type = self._get_approval_type(order.amount_total)

            if not approval_type:
                raise ValidationError("No approval category is configured for this amount. Please set up approval categories.")

            if order.approval_request_id:
                if order.approval_request_id.request_status == "approved":
                    raise ValidationError("This order is already approved. You cannot request approval again.")
                
                if order.approval_request_id.request_status in ["waiting", "pending"]:
                    order.approval_request_id.write({"request_status": "cancel"})
                    
                order.approval_request_id = False  
                order.approval_request_id.unlink()

            order.approval_id = approval_type.id
            order.show_approval_type = True

            order.approval_request_id = self.env["approval.request"].create({
                "name": f"Approval Request for {order.name}",
                "category_id": approval_type.id,
                "amount": order.amount_total,
                "request_owner_id": self.env.user.id,
                "sale_order_id": order.id
            })

            order.needs_approval = False
            order.approval_request_id.action_confirm()

    def action_confirm(self):
        """
            Ensure approval is required before confirming the sale order.
        """
        for order in self:
            if not order.approval_request_id or order.approval_status != "approved":
                raise UserError("Order must be sent for approval and fully approved before confirmation.")
            
        return super().action_confirm()
