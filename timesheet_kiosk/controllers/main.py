from odoo import http
from odoo.http import request


class TimesheetKioskController(http.Controller):

    @http.route('/timesheet_kiosk/get_employee_data', type='json', auth='user')
    def get_employee_data(self, barcode):
        employee = request.env['hr.employee'].sudo().search_read(
            [['barcode', '=', barcode]],
            ['id', 'name', 'user_id'],
            
        )
        if not employee:
            return {'error': 'Employee not found'}

        employee = employee[0]
        user_id = employee['user_id'][0]

        tasks = request.env['project.task'].search_read(
            [['user_ids', 'in', [user_id]], ['stage_id.fold', '=', False]],
            ['id', 'name', 'project_id'],
        )

        task_ids = [t['id'] for t in tasks]
        timmer_data = request.env['timer.timer'].sudo().search_read(
            [
                ('parent_res_id', 'in', task_ids),
                ('parent_res_model', '=', 'project.task'),
            ],
            ['id', 'parent_res_id', 'res_id'],
        )

        timer_task_id = None
        timer_line_id = None
        timmer_project = {}

        if timmer_data:
            timer_task_id = timmer_data[0]['parent_res_id']
            timer_line_id = timmer_data[0]['res_id']
            timmer_data = True
            for task in tasks:
                if task['id'] == timer_task_id:
                    timmer_project = {'id': task['project_id'][0], 'name': task['project_id'][1]}
                    break
        else:
            timmer_data = False


        projects = {}
        for task in tasks:
            pid, pname = task['project_id']
            if pid not in projects:
                projects[pid] = {'id': pid, 'name': pname}

        return {
            'employee': employee,
            'tasks': tasks,
            'timer': timmer_data,
            'timertask': timer_task_id,
            'timerlineid': timer_line_id,
            'timmerproject': timmer_project,
            'projects': list(projects.values()),
        }

    @http.route('/timesheet_kiosk/stop_timer', type='json', auth='user')
    def stop_timer(self, timer_line_id, employee_id):
        config = request.env['ir.config_parameter'].sudo()
        max_hours = float(config.get_param(
            'timesheet_kiosk.timesheet_kiosk_max_hours', 8.0
        ))

        line = request.env['account.analytic.line'].sudo().browse(timer_line_id)
        line.action_timer_stop()

        vals = {
            'name': 'Work done',
            'employee_id': employee_id,
        }
        if line.unit_amount > max_hours:
            vals['unit_amount'] = max_hours

        line.write(vals)

        template_id = int(config.get_param(
            'timesheet_kiosk.timesheet_kiosk_email_template_id', 0
        ))
        if template_id and line.project_id.user_id:
            template = request.env['mail.template'].sudo().browse(template_id)
            template.send_mail(line.id, force_send=True)

        return {'success': True}
