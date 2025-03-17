# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http, fields
from odoo.http import request


class TimesheetController(http.Controller):

    @http.route("/timesheet/create", type="json", auth="user")
    def create_timesheet(self, **kwargs):
        """Create a new timesheet entry when the timer starts."""
        try:
            params = kwargs.get("params", kwargs)
            project_id = params.get("project_id")
            task_id = params.get("task_id")
            employee_id = params.get("employee_id")

            new_timesheet = request.env["account.analytic.line"].sudo().create({
                "project_id": project_id,
                "task_id": task_id,
                "employee_id": employee_id,
                "name": "Work in Progress",
                "unit_amount": 0.0,
                "date": fields.Date.today(),
                "timer_active": True,
                "timer_start_time": fields.Datetime.now(),
            })

            return {"id": new_timesheet.id, "name": new_timesheet.name}
        except KeyError as error:
            return {"id": False, "error": str(error)}

    @http.route("/timesheet/stop", type="json", auth="user")
    def stop_timesheet(self, **kwargs):
        """Stop the timer, record hours worked, and notify the project manager via email."""
        try:
            params = kwargs.get("params", kwargs)
            timesheet_id = params.get("timesheet_id")
            timesheet = request.env["account.analytic.line"].browse(timesheet_id)

            if not timesheet.exists():
                return {"id": False, "error": "Timesheet not found"}

            if timesheet.employee_id.user_id != request.env.user and not request.env.user._is_admin():
                return {"error": "Access denied"}

            max_work_hours_per_day = float(
                request.env["ir.config_parameter"]
                .sudo()
                .get_param("time_tracking_kiosk.max_work_hours_per_day", 8)
            )

            start_time = timesheet.timer_start_time
            end_time = fields.Datetime.now()
            hours_worked = (end_time - start_time).total_seconds() / 3600
            hours_worked = min(hours_worked, max_work_hours_per_day)

            timesheet.sudo().write({
                "unit_amount": hours_worked,
                "name": "Work Done",
                "timer_active": False,
            })

            project_manager = timesheet.task_id.project_id.user_id
            if project_manager:
                email_template = request.env.ref(
                    "time_tracking_kiosk.email_template_pm_notification",
                    raise_if_not_found=True,
                )
                email_template.sudo().send_mail(timesheet.id, force_send=True)

            return {
                "id": timesheet.id,
                "unit_amount": timesheet.unit_amount,
                "name": timesheet.name,
            }
        except KeyError as error:
            return {"id": False, "error": str(error)}
