from datetime import datetime
from odoo import Command, api, fields, models

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    recurring_frequency  = fields.Selection([('weekly', 'Weekly'), ('bi_weekly', 'Bi Weekly'), ('monthly', 'Monthly'), ('preferred_day','Preferred Day')])
    preferred_day = fields.Selection([('monday', 'Monday'), ('tuesday', 'Tuesday'), ('wednesday', 'Wednesday'), ('thursday','Thursday'), ('friday','Friday'), ('saturday','Saturday'), ('sunday','Sunday')])

    @api.onchange('recurring_frequency')
    def _onchange_recurring_frequency(self):
        if (self.recurring_frequency!='preferred_day'):
            self.preferred_day = False

    def write(self, values):
        project = self.project_id
        if not project or not values.get('end_date'):
            return super().write(values)

        end_date = values.get('end_date')
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        old_end_date = self.end_date
        result = super().write(values)
        if end_date < old_end_date:
            self._unlink_old_tasks(end_date)
        else:
            for line in self.order_line:
                line._timesheet_create_task(line.product_id.project_id)
    
        return result

    def _unlink_old_tasks(self, new_task_date):
        """ Unlink tasks if their new date_deadline is earlier than the existing one. 

        :param sale_order: current sale order
        :param new_task_date: new end date of sale order
        """
        tasks_to_unlink = []
        for task in self.tasks_ids:
            if new_task_date < task.date_deadline.date():
                tasks_to_unlink.append(task)

        if tasks_to_unlink:
            self.project_id.write({'tasks': [Command.unlink(task.id) for task in tasks_to_unlink]})