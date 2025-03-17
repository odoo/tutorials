# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.tests.common import tagged
from odoo import fields
from datetime import datetime, timedelta
from odoo.tests import HttpCase
import json
import time


@tagged('post_install', '-at_install')
class TimesheetKioskTestCase(HttpCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.test_user = cls.env['res.users'].create({
            'login': 'test_employee_user',
            'name': 'Test Employee User',
            'email': 'test@example.com',
            'password': 'test_employee_user',
            'company_id': cls.env.company.id,
        })

        cls.test_employee = cls.env['hr.employee'].create({
            'name': 'Test Employee',
            'barcode': '12345',
            'user_id': cls.test_user.id,
        })

        cls.test_project = cls.env['project.project'].create({
            'name': 'Test Project',
            'user_id': cls.env.user.id,
        })

        cls.test_task = cls.env['project.task'].create({
            'name': 'Test Task',
            'project_id': cls.test_project.id,
            'user_ids': [(6, 0, [cls.env.user.id])],
        })

        cls.initial_timesheet = cls.env['account.analytic.line'].create({
            'project_id': cls.test_project.id,
            'task_id': cls.test_task.id,
            'employee_id': cls.test_employee.id,
            'name': 'Initial Timesheet',
            'unit_amount': 0.0,
            'date': fields.Date.today(),
            'timer_active': False,
        })

    def send_json_post_request(self, url, payload):
        """Send a JSON POST request and return the parsed JSON response."""
        response = self.url_open(
            url=url,
            data=json.dumps(payload),
            headers={'Content-Type': 'application/json'},
        )
        return response.json()

    def test_create_timesheet(self):
        """Test the creation of a timesheet via the controller."""
        payload = {
            'params': {
                'project_id': self.test_project.id,
                'task_id': self.test_task.id,
                'employee_id': self.test_employee.id,
            },
        }
        self.authenticate('test_employee_user', 'test_employee_user')
        response = self.send_json_post_request('/timesheet/create', payload)

        self.assertIn('result', response, "Response should contain a 'result' key")
        self.assertIn('id', response['result'], "Result should contain an 'id' key")
        self.assertTrue(response['result']['id'], "Timesheet ID should be truthy")

        created_timesheet = self.env['account.analytic.line'].browse(response['result']['id'])
        self.assertTrue(created_timesheet.exists())
        self.assertEqual(created_timesheet.project_id, self.test_project)
        self.assertEqual(created_timesheet.task_id, self.test_task)
        self.assertEqual(created_timesheet.employee_id, self.test_employee)
        self.assertTrue(created_timesheet.timer_active)

    def test_stopping_a_timesheet_updates_unit_amount(self):
        """Test stopping a timesheet updates the unit_amount field."""
        start_time = fields.Datetime.now()
        timesheet = self.env['account.analytic.line'].create({
            'project_id': self.test_project.id,
            'task_id': self.test_task.id,
            'employee_id': self.test_employee.id,
            'name': 'Work in Progress',
            'unit_amount': 0.0,
            'date': fields.Date.today(),
            'timer_active': True,
            'timer_start_time': start_time,
        })
        self.authenticate('test_employee_user', 'test_employee_user')
        time.sleep(1)
        response = self.send_json_post_request('/timesheet/stop', {
            'params': {
                'timesheet_id': timesheet.id,
            },
        })
        updated_timesheet = self.env['account.analytic.line'].browse(response['result']['id'])
        self.assertIsNotNone(updated_timesheet)
        self.assertFalse(updated_timesheet.timer_active)
        self.assertGreater(updated_timesheet.unit_amount, 0.0)

    def test_stopping_a_timesheet_respects_max_hours(self):
        """Test stopping a timesheet respects configured max hours."""
        max_hours = 1
        self.env['ir.config_parameter'].sudo().set_param('time_tracking_kiosk.max_work_hours_per_day', max_hours)
        start_time = datetime.now() - timedelta(hours=2)
        timesheet = self.env['account.analytic.line'].create({
            'project_id': self.test_project.id,
            'task_id': self.test_task.id,
            'employee_id': self.test_employee.id,
            'name': 'Work in Progress',
            'unit_amount': 0.0,
            'date': fields.Date.today(),
            'timer_active': True,
            'timer_start_time': start_time,
        })
        self.authenticate('test_employee_user', 'test_employee_user')
        response = self.send_json_post_request('/timesheet/stop', {
            'params': {
                'timesheet_id': timesheet.id,
            },
        })
        updated_timesheet = self.env['account.analytic.line'].browse(response['result']['id'])
        self.assertEqual(updated_timesheet.unit_amount, max_hours)
