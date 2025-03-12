from odoo import api, fields, models


class SaleSubscriptionPlan(models.Model):
    _inherit = 'sale.subscription.plan'
    _order = 'sequence, billing_period_value'

    sequence = fields.Integer(compute='_compute_sequence', store=True)

    @api.depends('billing_period_unit')
    def _compute_sequence(self):
        """Assigns sequence to subscription plans based on billing period unit."""
        unit_order = {'week': 1, 'month': 2, 'year': 3}
        
        for plan in self:
            plan.sequence = unit_order.get(plan.billing_period_unit, 99)
