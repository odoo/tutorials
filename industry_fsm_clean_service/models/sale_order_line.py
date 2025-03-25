# Part of Odoo. See LICENSE file for full copyright and licensing details.

import pytz
from datetime import datetime, timedelta
from odoo import models, _

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def _timesheet_create_task(self, project):
        """Generate recurring FSM tasks based on sale order settings.
            :param project: record of project.project in which the task should be created
            :return task: record of the created task
        """
        sale_order = self.order_id
        if not sale_order.recurring_task_frequency:
            return super()._timesheet_create_task(project)

        user_tz = pytz.timezone(self.env.user.tz or 'UTC')
        start_date = sale_order.date_order.astimezone(user_tz)
        end_datetime = datetime.combine(sale_order.end_date, datetime.max.time()).astimezone(user_tz)

        resource_work_intervals, _ = self.env.user.resource_ids._get_valid_work_intervals(start_date, end_datetime)
        work_intervals = sorted({
            (int(interval[2].dayofweek), int(interval[2].hour_from), int(interval[2].hour_to))
            for _, intervals in resource_work_intervals.items()
            for interval in intervals
        })

        service_lines = self.filtered(lambda line: line.product_id.type == 'service' and line.product_id.id)
        interval_days = {'weekly': 7, 'biweekly': 14, 'monthly': 30}.get(sale_order.recurring_task_frequency, 7)

        created_tasks_map = {}
        task_values = []
        end_date = sale_order.end_date or (sale_order.date_order + timedelta(days=interval_days))
        task_date = sale_order.date_order + timedelta(days=1)

        preferred_weekday = None
        if sale_order.preferred_day:
            weekdays_list = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
            preferred_weekday = weekdays_list.index(sale_order.preferred_day)

        while task_date.date() <= end_date:
            initial_date = task_date
            task_date = self._get_next_valid_task_date(task_date, work_intervals, preferred_weekday)
            for line in service_lines:
                service_id = line.product_id.id
                key = (task_date.date(), service_id)

                if key not in created_tasks_map and task_date.date() <= end_date:
                    task_values.append({
                        'name': f"{sale_order.name} - {line.product_id.name}",
                        'project_id': project.id,
                        'sale_line_id': line.id,
                        'planned_date_begin': task_date,
                        'date_deadline': task_date + timedelta(hours=1),
                        'allocated_hours': 1.0,
                        'description': (line.name.split("\n", 1)[1] if "\n" in line.name else ""),
                    })
                    created_tasks_map[key] = True

            task_date = initial_date + timedelta(days=interval_days)

        if task_values:
            created_tasks = self.env['project.task'].sudo().create(task_values)
            sale_order.tasks_ids = [(6, 0, created_tasks.ids)]

        return sale_order.tasks_ids

    def _get_next_valid_task_date(self, task_date, work_intervals, preferred_weekday):
        """Find the next valid workday for task scheduling, avoiding holidays.
            :param task_date: The date on which the task will be created.
            :param work_intervals: A set of valid working hours.
            :param preferred_day: An integer representing the preferred day on which the task should be created.
            :return: The adjusted task date that meets the specified conditions.
        """
        public_holidays = self.env['resource.calendar.leaves'].search([
            ('resource_id', '=', False),
            ('company_id', '=', self.env.company.id),
        ])

        if preferred_weekday is not None:
            days_to_add = (preferred_weekday - task_date.weekday()) % 7
            task_date += timedelta(days=days_to_add or 7)

        while True:
            if any(holiday.date_from.date() <= task_date.date() <= holiday.date_to.date() for holiday in public_holidays):
                task_date += timedelta(days=1)
                continue

            if work_intervals:
                valid_intervals = [
                    interval
                    for interval in work_intervals
                    if task_date.weekday() == interval[0]
                ]
                if valid_intervals:
                    in_valid_interval = any(
                        hour_from <= task_date.hour < hour_to
                        for _, hour_from, hour_to in valid_intervals
                    )
                    if not in_valid_interval:
                        hour_from = valid_intervals[0][1]
                        task_date = task_date.replace(
                            hour=hour_from, minute=0, second=0, microsecond=0
                        )
                    return task_date
            else:
                return task_date

            sorted_weekdays = sorted({interval[0] for interval in work_intervals})
            next_day = min((day for day in sorted_weekdays if day > task_date.weekday()), default=sorted_weekdays[0])
            task_date += timedelta(days=(next_day - task_date.weekday()) % 7 or 7)
