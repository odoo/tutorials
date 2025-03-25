# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    recurring_task_frequency = fields.Selection([
        ('weekly', "Weekly"),
        ('biweekly', "BiWeekly"),
        ('monthly', "Monthly"),
        ('preferred_day', "Preferred Day"),
    ], string="Recurring Task Frequency",
       default='weekly',
       help="Defines the frequency at which recurring tasks will be generated for this order.")

    preferred_day = fields.Selection([
        ('monday', "Monday"),
        ('tuesday', "Tuesday"),
        ('wednesday', "Wednesday"),
        ('thursday', "Thursday"),
        ('friday', "Friday"),
        ('saturday', "Saturday"),
        ('sunday', "Sunday"),
    ], string="Preferred Day",
       default='monday',
       help="If 'Preferred Day' is selected as the frequency, this specifies the preferred day of the week.")

    show_recurring_fields = fields.Boolean(
        compute='_compute_show_recurring_fields',
        store=True
    )

    @api.depends('order_line.product_id', 'order_line.product_id.service_tracking', 'order_line.product_id.project_id.is_fsm')
    def _compute_show_recurring_fields(self):
        for order in self:
            order.show_recurring_fields = any(
                line.product_id.type == 'service' and
                line.product_id.service_tracking in ['task', 'task_global_project'] and
                line.product_id.project_id and line.product_id.project_id.is_fsm
                for line in order.order_line
            )
