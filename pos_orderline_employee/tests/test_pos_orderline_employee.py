from odoo.tests import tagged
from odoo.addons.point_of_sale.tests.test_frontend import TestPointOfSaleHttpCommon

@tagged('-at_install', 'post_install') 
class TestPosOrderlineEmployeeTour(TestPointOfSaleHttpCommon):
    
    def test_pos_add_employee_to_orderline(self):
        self.env['hr.employee'].create([
            {
                'name': 'Employee Test 1',
                'work_email': 'employee1@example.com',
                'mobile_phone': '9898989001',
            },
            {
                'name': 'Employee Test 2',
                'work_email': 'employee2@example.com',
                'mobile_phone': '9898989002',
            },
            {
                'name': 'Employee Test 3',
                'work_email': 'employee3@example.com',
                'mobile_phone': '9898989003',
            },
            {
                'name': 'Employee Test 4',
                'work_email': 'employee4@example.com',
                'mobile_phone': '9898989004',
            }
        ])
        
        self.start_tour("/pos/ui?config_id=%d" % self.main_pos_config.id, 'PosAddEmployeeToOrderline', login="pos_user")
        
    def test_employee_all_fields_displayed(self):
        self.env["hr.employee"].create({
            "name": "Employee Test 5",
            "mobile_phone": "9898989005",
            "work_email": "employee5@example.com"
        })
        
        self.env["hr.employee"].create({
            "name": "Mustafa Kapasi",
            "mobile_phone": "9898989006",
            "work_email": "mustafa@example.com"
        })

        self.start_tour("/pos/ui?config_id=%d" % self.main_pos_config.id, 'PosEmployeeAllFieldsDisplayed', login="pos_user")
