import pytz
from datetime import datetime, timedelta

from odoo import Command, _, models
from odoo.exceptions import ValidationError


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _timesheet_create_task(self, project):
        sale_order = self.order_id
        if not sale_order.recurring_frequency:
            return super()._timesheet_create_task(project)
        if (sale_order.recurring_frequency != "preferred_day" and sale_order.preferred_day ): 
            raise ValidationError(_("Preferred day can only be set if the recurring frequency is Preferred Day."))

        user_tz = pytz.timezone(self.env.user.tz or "UTC")
        start_date = sale_order.date_order.astimezone(user_tz)
        end_datetime = datetime.combine(sale_order.end_date, datetime.max.time())
        end_datetime = end_datetime.astimezone(user_tz)
        resource_work_intervals, _calendar_intervals = (
            self.env.user.resource_ids._get_valid_work_intervals(
                start_date, end_datetime
            )
        )
        work_intervals = set()
        for _resource_id, intervals in resource_work_intervals.items():
            for interval in intervals:
                work_intervals.add(
                    (
                        int(interval[2].dayofweek),
                        int(interval[2].hour_from),
                        int(interval[2].hour_to),
                    )
                )

        work_intervals = sorted(work_intervals)
        service_lines = self.filtered(
            lambda line: line.product_id.type == "service"
        )
        weekdays_list = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        interval = {"weekly": 7, "bi_weekly": 14, "monthly": 30}.get(
            sale_order.recurring_frequency, 7)
        end_date = (
            sale_order.end_date
            or sale_order.date_order + timedelta(days=interval)
        )
        task_date = sale_order.date_order + timedelta(days=1)
        preferred_weekday = (
            weekdays_list.index(sale_order.preferred_day)
            if sale_order.preferred_day
            else None
        )
        existing_task_dates = {
            (task.planned_date_begin.replace(hour=0, minute=0, second=0, microsecond=0), task.sale_line_id.product_id.id) 
            for task in sale_order.tasks_ids
        }
        last_task_date_per_product = self.get_last_task_date_per_product(sale_order, task_date)
        public_holidays = self.env.user.employee_id._get_public_holidays(start_date, end_datetime)
        last_task_date = last_task_date_per_product.get(self.product_id.id, task_date)
        task_date=last_task_date
        while task_date.date() <= end_date:
            initial_date = task_date
            task_date = self.get_task_date(public_holidays,task_date, work_intervals, preferred_weekday)
            for line in service_lines:
                key = (task_date.replace(hour=0, minute=0, second=0, microsecond=0), line.product_id.id)
                if key not in existing_task_dates and task_date.date() <= end_date and task_date.date() >= last_task_date.date():
                    task = self.env["project.task"].create(
                        {
                            "name": f"{sale_order.name} - {line.product_id.name}",
                            "project_id": project.id,
                            "sale_line_id": line.id,
                            'planned_date_begin': task_date,
                            "date_deadline": task_date + timedelta(hours=self.product_uom_qty),
                            "description": "".join(line.name.split("\n")[1:]),
                        }
                    )
                    sale_order.tasks_ids = [Command.link(task.id)]
                    existing_task_dates.add(key)

            task_date = initial_date + timedelta(days=interval)

        return sale_order.tasks_ids

    def is_holiday(self, public_holidays, task_date):
        return next(
            (
                holiday for holiday in public_holidays if holiday.date_from.date() <= task_date.date() <= holiday.date_to.date()
            ),
            None,
        )

    def get_task_date(self, public_holidays, task_date, work_intervals, preferred_day):
        """Calculate the task date, ensuring it falls on the preferred day, avoids holidays, and has a valid work interval.
        :param public_holidays: 
        :param task_date: The date on which the task will be created.
        :param work_intervals: A set of valid working hours.
        :param preferred_day: An integer representing the preferred day on which the task should be created.
        :return: The adjusted task date that meets the specified conditions.
        """
        if preferred_day:
            days_to_add = (preferred_day - task_date.weekday()) % 7
            task_date += timedelta(days=days_to_add)

        while True:
            # if it's a holiday
            matching_holiday = self.is_holiday(public_holidays, task_date)
            while matching_holiday:
                task_date = matching_holiday.date_to + timedelta(days=1)
                matching_holiday = self.is_holiday(public_holidays, task_date)
            # if it's a valid date
            if work_intervals:
                valid_intervals = [
                    interval
                    for interval in work_intervals
                    if task_date.weekday() == interval[0]
                ]
                if valid_intervals:
                    in_valid_interval = any(
                        hour_from <= task_date.hour < hour_to
                        for _day, hour_from, hour_to in valid_intervals
                    )
                    if not in_valid_interval:
                        hour_from = valid_intervals[0][1]
                        task_date = task_date.replace(
                            hour=hour_from, minute=0, second=0, microsecond=0
                        )
                    return task_date
            else:
                return task_date

            # update the date
            sorted_weekdays = sorted({interval[0] for interval in work_intervals})
            next_day = min((day for day in sorted_weekdays if day > task_date.weekday()), default=sorted_weekdays[0])
            task_date += timedelta(days=(next_day - task_date.weekday()) % 7)

    def update_task_date(self,qty):
        project=self.order_id.project_id
        for task in project.tasks:
            new_deadline = task.planned_date_begin + timedelta(hours=qty)
            task.write({'date_deadline': new_deadline})   

    def write(self,values):
        result = super().write(values)
        if 'product_uom_qty' in values:
            self.update_task_date(values.get('product_uom_qty'))
        return result

    def get_last_task_date_per_product(self, sale_order, default_date):
        """
        Get the last task date for each product in the sale order.
        :param sale_order: Sale Order object
        :param default_date: Default task date if no tasks exist
        :return: Dictionary with product_id as key and last task date as value
        """
        existing_task_dates = {}
        for task in sale_order.tasks_ids:
            product_id = task.sale_line_id.product_id.id
            task_deadline = task.date_deadline
            if product_id in existing_task_dates:
                existing_task_dates[product_id] = max(existing_task_dates[product_id], task_deadline)
            else:
                existing_task_dates[product_id] = task_deadline
        
        return existing_task_dates or {product_id: default_date for product_id in sale_order.order_line.mapped('product_id.id')}
