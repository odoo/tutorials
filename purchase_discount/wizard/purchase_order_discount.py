from odoo import api, fields, models
from odoo.exceptions import ValidationError


class PurchaseOrderDiscount(models.TransientModel):
    _name = 'purchase.order.discount'
    _description = "Discount Wizard"

    purchase_order_id = fields.Many2one(
        'purchase.order',
        default=lambda self: self.env.context.get('active_id'),
        required=True,
    )
    discount_percentage = fields.Float(string="Percentage")
    discount_type = fields.Selection(
        selection=[
            ('percentage', "%"),
            ('amount', "₹"),
        ],
        default='percentage',
    )
    percentage = fields.Float(compute='_compute_initial_discount')

    @api.constrains('discount_type', 'discount_percentage')
    def _check_discount_amount(self):
        for wizard in self:
            if (
                (wizard.discount_type in ('percentage')
                and wizard.discount_percentage > 100.0)
                or (wizard.discount_type in ('amount')
                and wizard.discount_percentage > wizard.purchase_order_id.amount_untaxed)
            ):
                raise ValidationError("Invalid discount amount")

    @api.depends('discount_type', 'discount_percentage')
    def _compute_initial_discount(self):
        if self.discount_type == 'amount':
            if self.purchase_order_id.amount_untaxed == 0:
                raise ValidationError("No more discount possible")
            self.percentage = (
                self.discount_percentage * 100 / self.purchase_order_id.amount_untaxed
            )
        else:
            self.percentage = self.discount_percentage

    def action_apply_discount(self):
        self.ensure_one()
        if self.discount_type == 'amount':
            self.purchase_order_id.order_line.write(
                {
                    'discount': (
                        self.discount_percentage
                        * 100
                        / self.purchase_order_id.amount_untaxed
                    )
                }
            )
        else:
            self.purchase_order_id.order_line.write(
                {'discount': self.discount_percentage}
            )
