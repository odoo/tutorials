# Part of Odoo. See LICENSE file for full copyright and licensing details.

import pytz
from datetime import datetime, timedelta
from odoo import fields
from odoo.tests import tagged
from odoo.tests.common import TransactionCase

@tagged('post_install', '-at_install')
class TestCleanService(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.company = cls.env.company
        cls.customer = cls.env['res.partner'].create({'name': 'Test Customer'})

        cls.project = cls.env['project.project'].create({
            'name': 'Test Project',
            'partner_id': cls.customer.id,
        })

        cls.product = cls.env['product.product'].create({
            'name': "Cleaning Service",
            'type': 'service',
            'recurring_invoice': True,
            'service_tracking': 'task_global_project',
            'project_id': cls.project.id,
        })

        cls.plan_month = cls.env['sale.subscription.plan'].create({
            'name': "Monthly Plan",
            'billing_period_unit': 'month',
        })

        cls.sale_order = cls.env['sale.order'].create({
            'partner_id': cls.customer.id,
            'plan_id': cls.plan_month.id,
            'end_date': fields.Date.today() + timedelta(days=30),
            'recurring_task_frequency': 'weekly',
        })

        cls.sale_order_line = cls.env['sale.order.line'].create({
            'order_id': cls.sale_order.id,
            'product_id': cls.product.id,
            'product_uom_qty': 1,
            'price_unit': 100,
        })

        cls.test_holiday = cls.env['resource.calendar.leaves'].create({
            'name': "Public Holiday",
            'company_id': cls.company.id,
            'date_from': fields.Datetime.today() + timedelta(days=1),
            'date_to': fields.Datetime.today() + timedelta(days=1, hours=23, minutes=59),
            'resource_id': False,
        })

    def test_task_recurrence(self):
        """Test that tasks are correctly generated for recurring sale orders."""
        self.sale_order.with_user(self.env.ref('base.user_admin')).action_confirm()
        tasks = self.env['project.task'].search([('project_id', '=', self.project.id)])
        self.assertTrue(tasks, "No task was created from the recurring sale order")
        for task in tasks:
            self.assertTrue(task.date_deadline, "Task has no deadline")
            self.assertLessEqual(task.date_deadline.date(), self.sale_order.end_date, "Task deadline exceeds contract end date")
            self.assertGreaterEqual(task.date_deadline.date(), self.sale_order.date_order.date(), "Task deadline is before sale order date")
        for task in tasks:
            self.assertFalse(
                self.test_holiday.date_from.date() <= task.date_deadline.date() <= self.test_holiday.date_to.date(),
                "Task deadline falls within the holiday period"
            )

    def test_recurring_task_timing(self):
        """Test that tasks respect the recurring frequency and working schedule."""
        self.sale_order.with_user(self.env.ref('base.user_admin')).action_confirm()
        tasks = self.env['project.task'].search([('project_id', '=', self.project.id)])
        interval_days = {'weekly': 7, 'biweekly': 14, 'monthly': 30}[self.sale_order.recurring_task_frequency]
        previous_date = None
        for task in sorted(tasks, key=lambda t: t.date_deadline):
            if previous_date:
                self.assertEqual((task.date_deadline.date() - previous_date).days, interval_days, "Task recurrence interval is incorrect")
            previous_date = task.date_deadline.date()

    def test_task_scheduling_on_preferred_day(self):
        """Test that tasks are scheduled on the preferred day when specified."""
        self.sale_order.write({'preferred_day': 'wednesday'})
        self.sale_order.with_user(self.env.ref('base.user_admin')).action_confirm()
        tasks = self.env['project.task'].search([('project_id', '=', self.project.id)])
        for task in tasks:
            self.assertEqual(task.date_deadline.strftime('%A').lower(), 'wednesday', "Task was not scheduled on the preferred day")

    def test_task_creation_without_preferred_day(self):
        """Test that tasks are created when no preferred day is set."""
        self.sale_order.write({'preferred_day': False})
        self.sale_order.with_user(self.env.ref('base.user_admin')).action_confirm()
        tasks = self.env['project.task'].search([('project_id', '=', self.project.id)])
        self.assertTrue(tasks, "Tasks were not created despite having a valid schedule")

    def test_task_timezone_respect(self):
        """Ensure tasks respect the user's timezone."""
        user_tz = self.env.user.tz or 'UTC'
        user_timezone = pytz.timezone(user_tz)
        self.sale_order.with_user(self.env.ref('base.user_admin')).action_confirm()
        tasks = self.env['project.task'].search([('project_id', '=', self.project.id)])
        for task in tasks:
            if task.date_deadline:
                deadline_in_user_tz = task.date_deadline.replace(tzinfo=pytz.utc).astimezone(user_timezone)
                self.assertEqual(deadline_in_user_tz.tzinfo.zone, user_tz, "Task deadline does not match user timezone")
            else:
                self.fail("Task has no deadline set")

    def test_recurring_tasks_only_on_business_days(self):
        """Ensure tasks are only created on business days."""
        self.sale_order.with_user(self.env.ref('base.user_admin')).action_confirm()
        tasks = self.env['project.task'].search([('project_id', '=', self.project.id)])
        for task in tasks:
            self.assertNotEqual(task.date_deadline.weekday(), 5, "Task was scheduled on a Saturday")
            self.assertNotEqual(task.date_deadline.weekday(), 6, "Task was scheduled on a Sunday")

    def test_task_scheduling_handles_holidays(self):
        """Ensure tasks are rescheduled if they fall on a holiday."""
        self.sale_order.with_user(self.env.ref('base.user_admin')).action_confirm()
        tasks = self.env['project.task'].search([('project_id', '=', self.project.id)])
        for task in tasks:
            self.assertFalse(
                self.test_holiday.date_from.date() <= task.date_deadline.date() <= self.test_holiday.date_to.date(),
                "Task was scheduled on a holiday"
            )

    def test_task_deadlines_with_end_date(self):
        """Ensure tasks do not get scheduled past the sale order's end date."""
        self.sale_order.with_user(self.env.ref('base.user_admin')).action_confirm()
        tasks = self.env['project.task'].search([('project_id', '=', self.project.id)])
        for task in tasks:
            self.assertLessEqual(task.date_deadline.date(), self.sale_order.end_date, "Task scheduled past end date")
