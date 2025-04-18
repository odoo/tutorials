# models/product_template.py
from odoo import models, fields


class SaleSubscriptionPlanInherit(models.Model):
    _inherit = 'sale.subscription.plan'

    # Add the Many2one field for the product template
    product_template_id = fields.Many2one(
        'product.template', string="Product Template", required=True, ondelete='cascade',
        help="The product template to which this subscription plan belongs."
    )

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    accept_one_time = fields.Boolean(
        string="Accept One-Time",
        help="Allow this subscription product to be sold as a one-time purchase."
    )
    subscription_plan_ids = fields.One2many(
        'sale.subscription.plan', 'product_template_id',
        string="Subscription Plans"
    )
