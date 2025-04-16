from odoo.tests import TransactionCase


class TestPortalUserAccess(TransactionCase):

    def setUp(self):
        super().setUp()
        self.PortalWizardUser = self.env['portal.wizard.user']
        self.ResUsers = self.env['res.users']

        self.test_user = self.ResUsers.create({
            'name': 'Test Portal User',
            'login': 'test_user@example.com',
            'email': 'test_user@example.com',
            'groups_id': [(6, 0, [self.env.ref("base.group_portal").id])],
            'portal_access_so': False,
            'portal_access_quotes': False,
            'portal_access_rfq': False,
            'portal_access_po': False,
            'portal_access_invoices': False,
            'portal_access_projects': False,
            'portal_access_tasks': False,
        })

    def test_default_access_rights(self):
        self.assertFalse(self.test_user.portal_access_so, "Sales Order Access should be False by default")
        self.assertFalse(self.test_user.portal_access_quotes, "Quotation Access should be False by default")
        self.assertFalse(self.test_user.portal_access_rfq, "RFQ Access should be False by default")
        self.assertFalse(self.test_user.portal_access_po, "Purchase Order Access should be False by default")
        self.assertFalse(self.test_user.portal_access_invoices, "Invoices Access should be False by default")
        self.assertFalse(self.test_user.portal_access_projects, "Projects Access should be False by default")
        self.assertFalse(self.test_user.portal_access_tasks, "Tasks Access should be False by default")

    def test_update_access_rights(self):
        self.test_user.write({
            'portal_access_so': True,
            'portal_access_quotes': True,
            'portal_access_rfq': True,
            'portal_access_po': True,
            'portal_access_invoices': True,
            'portal_access_projects': True,
            'portal_access_tasks': True,
        })

        self.assertTrue(self.test_user.portal_access_so, "Sales Order Access should be True")
        self.assertTrue(self.test_user.portal_access_quotes, "Quotation Access should be True")
        self.assertTrue(self.test_user.portal_access_rfq, "RFQ Access should be True")
        self.assertTrue(self.test_user.portal_access_po, "Purchase Order Access should be True")
        self.assertTrue(self.test_user.portal_access_invoices, "Invoices Access should be True")
        self.assertTrue(self.test_user.portal_access_projects, "Projects Access should be True")
        self.assertTrue(self.test_user.portal_access_tasks, "Tasks Access should be True")

    def test_group_assignment(self):
        group_so = self.env.ref('portal_user_access_control.sales_order_group')
        group_quotes = self.env.ref('portal_user_access_control.quotetion')

        self.test_user.write({'portal_access_so': True, 'portal_access_quotes': True})

        self.assertIn(self.test_user, group_so.users, "User should be in Sales Order group")
        self.assertIn(self.test_user, group_quotes.users, "User should be in Quotation group")

    def test_group_removal(self):
        group_so = self.env.ref('portal_user_access_control.sales_order_group')

        self.test_user.write({'portal_access_so': True})
        self.assertIn(self.test_user, group_so.users, "User should be in Sales Order group after granting access")

        self.test_user.write({'portal_access_so': False})
        self.assertNotIn(self.test_user, group_so.users, "User should be removed from Sales Order group after revoking access")

    def test_portal_user_status(self):
        self.assertTrue(self.test_user.is_portal_user, "User should be marked as a portal user since they belong to the portal group")

    def test_wizard_grant_access(self):
        wizard_user = self.PortalWizardUser.create({
            'user_id': self.test_user.id,
            'sales_order': True,
            'quotetion': True,
            'rfq': False,
            'purchase_order': True,
            'invoices': False,
            'projects': True,
            'tasks': False,
        })

        wizard_user.action_grant_access()

        self.assertTrue(self.test_user.portal_access_so, "Sales Order Access should be granted")
        self.assertTrue(self.test_user.portal_access_quotes, "Quotation Access should be granted")
        self.assertFalse(self.test_user.portal_access_rfq, "RFQ Access should not be granted")
        self.assertTrue(self.test_user.portal_access_po, "Purchase Order Access should be granted")
        self.assertFalse(self.test_user.portal_access_invoices, "Invoices Access should not be granted")
        self.assertTrue(self.test_user.portal_access_projects, "Projects Access should be granted")
        self.assertFalse(self.test_user.portal_access_tasks, "Tasks Access should not be granted")
