from datetime import datetime ,timedelta
from odoo import fields
from odoo.tests.common import TransactionCase,new_test_user
from odoo.exceptions import ValidationError
from odoo.tests import tagged


@tagged('post_install', '-at_install')
class TestRecurringTask(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.company = cls.env.company
        cls.customer = cls.env['res.partner'].create({'name': 'Test Customer'})
        cls.project = cls.env['project.project'].create({
            'name': 'Test',
            'partner_id': cls.customer.id,
        })
        cls.product = cls.env['product.product'].create({
            'name': "Cleaning",
            'type': 'service',
            'recurring_invoice': True,
            'service_tracking': 'task_global_project',
            'project_id': cls.project.id
        })
        cls.plan_month = cls.env['sale.subscription.plan'].create({
            'name': "Monthly",
            'billing_period_unit': 'month',
        })
        cls.sale_order = cls.env['sale.order'].create({
            'partner_id': cls.customer.id,
            'plan_id': cls.plan_month.id,
            'end_date': fields.Date.today() + timedelta(days=30),
            'recurring_frequency': 'weekly',
        })
        cls.sale_order_line = cls.env['sale.order.line'].create({
            'order_id': cls.sale_order.id,
            'product_id': cls.product.id,
            'product_uom_qty': 1,
            'price_unit': 100,
        })
        cls.test_holiday = cls.env['resource.calendar.leaves'].create([{
            'name': "Public Holiday test",
            'company_id': cls.company.id,
            'date_from': fields.Datetime.today() + timedelta(days=1),  
            'date_to': fields.Datetime.today() + timedelta(days=1,hours=23,minutes=59,seconds=59),
            'resource_id': False,
        }])

    def test_preferred_day_validation(self):
        sale_order = self.env['sale.order'].create({
            'partner_id': self.customer.id,
            'plan_id': self.plan_month.id,
            'end_date': fields.Date.today() + timedelta(days=30),
            'recurring_frequency': 'weekly',
            'preferred_day': 'monday'
        })
        self.env['sale.order.line'].create({
            'order_id': sale_order.id,
            'product_id': self.product.id,
            'product_uom_qty': 1,
            'price_unit': 100,
        })
        with self.assertRaises(ValidationError):
            sale_order.action_confirm()

    def test_task_recurrence(self):
        self.sale_order.with_user(self.env.ref('base.user_admin')).action_confirm()

        tasks = self.env['project.task'].search([('project_id', '=', self.project.id)])
        self.assertTrue(tasks, "No task was created from recurring sale order")
        for task in tasks:
            self.assertTrue(task.date_deadline,"Task has no deadline")
            self.assertLessEqual(task.date_deadline.date(), self.sale_order.end_date, "Task deadline exceeds contract end date")
            self.assertGreaterEqual(task.date_deadline.date(), self.sale_order.date_order.date(), f"Task deadline exceeds contract end date")

        # Here we are checking the task_deadline for public holiday which is created above if this will true then we don't need to check for other tasks deadlines
        self.assertFalse(self.test_holiday.date_from <= tasks[0].date_deadline <= self.test_holiday.date_to,"task deadline falls within the holiday period")  
