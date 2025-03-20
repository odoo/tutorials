# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.tests.common import TransactionCase
from odoo.tests import tagged


@tagged('at_install')
class TestCrmContactDetails(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Create Parent Company
        cls.company = cls.env['res.partner'].create({
            'name': 'Main Company',
            'company_type': 'company',
        })

        # Create Addresses (Branches)
        cls.branch_1 = cls.env['res.partner'].create({
            'name': 'Branch 1',
            'parent_id': cls.company.id,
        })

        cls.branch_2 = cls.env['res.partner'].create({
            'name': 'Branch 2',
            'parent_id': cls.company.id,
        })

        # Create Contacts (Child Contacts)
        cls.contact_1 = cls.env['res.partner'].create({
            'name': 'John Doe',
            'type': 'contact',
            'parent_id': cls.branch_1.id,
            'show_in_contact_detail': True,
        })

        cls.contact_2 = cls.env['res.partner'].create({
            'name': 'Alice Smith',
            'type': 'contact',
            'parent_id': cls.branch_1.id,
            'show_in_contact_detail': False,
        })

        cls.contact_3 = cls.env['res.partner'].create({
            'name': 'Mike Johnson',
            'type': 'contact',
            'parent_id': cls.branch_2.id,
            'show_in_contact_detail': True,
        })

        # Create CRM Lead
        cls.lead = cls.env['crm.lead'].create({
            'name': 'Test Lead',
            'address_detail_ids': [(6, 0, [cls.branch_1.id, cls.branch_2.id])],
        })

    def test_contact_filtering_based_on_show_in_contact_detail(self):
        """Test if contact list updates when show_in_contact_detail is toggled."""
        self.contact_2.show_in_contact_detail = True  # Make Alice visible
        self.lead._compute_contact_details()
        self.assertIn(self.contact_2, self.lead.contact_detail_ids, "Alice Smith should be visible after enabling show_in_contact_detail")

    def test_contact_list_clears_when_no_addresses(self):
        """Test if contact list clears when no addresses are assigned."""
        self.lead.address_detail_ids = [(5,)]  # Remove all addresses
        self.lead._compute_contact_details()
        self.assertFalse(self.lead.contact_detail_ids, "contact_detail_ids should be empty when no addresses are assigned")

    def test_contact_list_updates_when_contact_is_removed(self):
        """Test if contacts update when a contact is deleted."""
        self.contact_1.unlink()  # Remove John Doe
        self.lead._compute_contact_details()
        self.assertNotIn(self.contact_1, self.lead.contact_detail_ids, "John Doe should not be in contact_detail_ids after deletion")

    def test_contact_list_updates_when_address_selection_changes(self):
        """Test if contact list updates when a different address is selected."""
        self.lead.address_detail_ids = [(6, 0, [self.branch_2.id])]  # Only select Branch 2
        self.lead._compute_contact_details()
        self.assertIn(self.contact_3, self.lead.contact_detail_ids, "Mike Johnson should be in contact_detail_ids")
        self.assertNotIn(self.contact_1, self.lead.contact_detail_ids, "John Doe should not be in contact_detail_ids since Branch 1 is removed")
