from odoo import api, fields, models


class HrTdsDeclarationWizard(models.TransientModel):
    _name = "hr.tds.declaration.wizard"
    _description = "Generate declaration wizard"

    selection_mode = fields.Selection(
        selection=[
            ("by_employee", "By Employee"),
            ("by_department", "By Department"),
            ("by_job_position", "By Job Position"),
            ("by_salary_structure", "By Salary Structure")
        ],
        string="Selection Mode",
        default="by_employee",
        required=True,
    )

    # Fields is used to show emplpoyees in list view according to filter is selected.
    employee_ids = fields.Many2many("hr.employee", "hr_employee_tds_rel", string="Employees Selection", compute="_compute_employee_id", store=True, readonly=False)
    # Field is used to select employee when selection mode is by_employee.
    employee_id = fields.Many2one("hr.employee", string="Employees")
    structure_id = fields.Many2one("hr.payroll.structure", string="Salary Structure")
    department_id = fields.Many2one("hr.department", string="Department")
    job_id = fields.Many2one("hr.job", string="Job Position")

    @api.depends("selection_mode", "structure_id", "department_id", "job_id", "employee_id")
    def _compute_employee_id(self):
        for wizard in self:
            domain = wizard._get_employee_domain()
            wizard.employee_ids = self.env["hr.employee"].search(domain)

    def _get_employee_domain(self):
        """Determines the domain for filtering employees based on the selected mode.

        This function constructs a domain filter based on the `selection_mode` and
        the corresponding selected field (`employee_id`, `department_id`, `job_id`, or `structure_id`).

        Returns:
            list: A domain list to filter employees in `hr.employee` based on the selection mode."""

        domain = [("company_id", "=", self.env.company.id)]  # Default domain
        if self.selection_mode == "by_employee" and self.employee_id:
            domain = [("id", "=", self.employee_id.id)]
        elif self.selection_mode == "by_department" and self.department_id:
            domain = [("department_id", "=", self.department_id.id)]
        elif self.selection_mode == "by_job_position" and self.job_id:
            domain = [("job_id", "=", self.job_id.id)]
        elif self.selection_mode == "by_salary_structure" and self.structure_id:
            domain = [("structure_type_id", "=", self.structure_id.type_id.id)]

        return domain

    def generate_tds_declaration(self):
        """Generates TDS declarations for selected employees based on their active contracts.

        This method retrieves the active TDS declaration from the context, fetches employees
        linked to it, and determines their valid contracts within the specified date range.
        It then creates TDS declaration details for each employee's contract.

        Updates the TDS declaration state to 'confirmed' upon successful creation."""

        tds_declaration = self.env["hr.tds.declaration"].browse(self.env.context.get("active_id"))
        employees = self.employee_ids
        contracts = employees._get_contracts(tds_declaration.start_date, tds_declaration.end_date, states=["open"])
        tds_declaration_details = []
        for contract in contracts:
            tds_declaration_details.append(
                {
                    "name": f"TDS Declaration - {contract.employee_id.name}",
                    "tds_declaration_id": tds_declaration.id,
                    "employee_id": contract.employee_id.id,
                    "contract_id": contract.id,
                    "start_date": tds_declaration.start_date,
                    "end_date": tds_declaration.end_date,
                    "financial_year": tds_declaration.financial_year,
                }
            )
        self.env["hr.tds.declaration.details"].create(tds_declaration_details)

        success_result = {
            "type": "ir.actions.act_window",
            "res_model": "hr.tds.declaration",
            "views": [[False, "form"]],
            "res_id": tds_declaration.id,
        }
        tds_declaration.state = "confirmed"

        return success_result
