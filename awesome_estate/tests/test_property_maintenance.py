from odoo.tests import TransactionCase, tagged


@tagged('standard')
class TestAwesomeEstateMaintenance(TransactionCase):
    """Test maintenance request lifecycle and computed fields."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Property = cls.env['awesome.estate.property']
        cls.Maintenance = cls.env['awesome.estate.property.maintenance']
        cls.Subtask = cls.env['awesome.estate.property.maintenance.subtask']
        cls.Cost = cls.env['awesome.estate.property.maintenance.cost']
        cls.Partner = cls.env['res.partner']

        cls.partner = cls.Partner.create({'name': 'Requester'})
        cls.property = cls.Property.create(
            {'name': 'Maint Test', 'expected_price': 100000, 'living_area': 80}
        )

        cls.request = cls.Maintenance.create(
            {
                'name': 'Leaky faucet',
                'property_id': cls.property.id,
                'issue_type': 'plumbing',
                'requester_id': cls.partner.id,
                'estimate_cost': 500,
            }
        )

    def test_maintenance_default_state(self):
        self.assertEqual(self.request.state, 'new')

    def test_maintenance_estimate_cost_from_issue_type(self):
        self.request.issue_type = 'electricity'
        self.request._onchange_issue_type()
        self.assertEqual(self.request.estimate_cost, 1000.0)

        self.request.issue_type = 'structural'
        self.request._onchange_issue_type()
        self.assertEqual(self.request.estimate_cost, 10000.0)

    def test_assign_technician(self):
        self.request.technician_id = self.env.user
        self.request._onchange_technician()
        self.assertEqual(self.request.state, 'assigned')

    def test_action_assign(self):
        self.request.technician_id = self.env.user
        self.request.action_assign()
        self.assertEqual(self.request.state, 'assigned')

    def test_action_start(self):
        self.request.technician_id = self.env.user
        self.request.action_assign()
        self.request.action_start()
        self.assertEqual(self.request.state, 'in_progress')

    def test_action_done(self):
        self.Subtask.create(
            {
                'maintenance_id': self.request.id,
                'name': 'Fix faucet',
                'state': 'done',
                'cost': 300.0,
            }
        )
        self.request.technician_id = self.env.user
        self.request.action_assign()
        self.request.action_start()
        self.request.action_done()
        self.assertEqual(self.request.state, 'done')
        self.assertTrue(self.request.close_date)

    def test_compute_actual_cost_from_subtasks(self):
        self.Subtask.create(
            {
                'maintenance_id': self.request.id,
                'name': 'Part A',
                'cost': 200.0,
                'state': 'done',
            }
        )
        self.Subtask.create(
            {
                'maintenance_id': self.request.id,
                'name': 'Part B',
                'cost': 150.0,
                'state': 'done',
            }
        )
        self.Cost.create(
            {
                'maintenance_id': self.request.id,
                'name': 'Service fee',
                'amount': 50.0,
            }
        )
        self.assertEqual(self.request.actual_cost, 400.0)

    def test_action_cancel_needs_reason(self):
        self.request.technician_id = self.env.user
        self.request.action_assign()
        with self.assertRaises(Exception):
            self.request.action_cancel()
        self.request.internal_notes = 'Cancel reason provided'
        self.request.action_cancel()
        self.assertEqual(self.request.state, 'canceled')

    def test_action_reset(self):
        self.request.action_cancel()
        self.request.action_reset()
        self.assertEqual(self.request.state, 'new')
        self.assertFalse(self.request.close_date)

    def test_compute_progress(self):
        self.request.technician_id = self.env.user
        self.request.action_assign()
        self.Subtask.create(
            {
                'maintenance_id': self.request.id,
                'name': 'Step 1',
                'state': 'done',
            }
        )
        self.Subtask.create(
            {
                'maintenance_id': self.request.id,
                'name': 'Step 2',
                'state': 'in_progress',
            }
        )
        self.assertEqual(self.request.progress, 50)
