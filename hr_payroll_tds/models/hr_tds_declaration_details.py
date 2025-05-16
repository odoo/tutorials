from odoo import api, fields, models


class HrTdsDeclarationDetails(models.Model):
    _name = "hr.tds.declaration.details"
    _description = "Hr TDS declaration  details for genearated employees"

    name = fields.Char(string="Tax Declarations")
    tds_declaration_id = fields.Many2one("hr.tds.declaration", string="TDS Declaration")
    employee_id = fields.Many2one("hr.employee")
    contract_id = fields.Many2one("hr.contract", string="Contract")
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    financial_year = fields.Char(string="Financial Year")
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("verify", "Confirmed"),
            ("approve", "Approved"),
            ("cancel", "Cancelled")
        ],
        string="Status",
        default="new"
    )
    tax_regime = fields.Selection(
        selection=[
            ("new_regime", "New Regime"),
            ("old_regiem", "Old Regime")
        ],
        string="Tax Regime",
        default="new_regime"
    )
    age_category = fields.Selection(
        selection=[
            ("lt60", "Less Than 60"),
            ("60to80", "60 - 80"),
            ("gt80", "Above 80")
        ],
        string="Category (Age)",
        default="lt60"
    )
    currency_id = fields.Many2one("res.currency", default=lambda self: self.env.company.currency_id.id)
    total_income = fields.Monetary(string="Total Income (yearly)", compute="_compute_total_income", inverse="_inverse_total_income", readonly=False, store=True)
    standard_deduction = fields.Monetary(
        string="Standard Deducation",
        default=lambda self: self.env['hr.rule.parameter']._get_parameter_from_code('l10n_in_standard_deduction_new_regime'),
        readonly=True)
    taxable_amount = fields.Monetary(string="Taxable Amount", compute="_compute_taxable_amount")
    tax_on_taxable_amount = fields.Monetary(string="Tax On Taxable Amount", compute="_compute_taxable_amount")
    rebate = fields.Monetary(string="Rebate Under Section 87A(a)", compute="_compute_taxable_amount")
    total_tax_on_income = fields.Monetary(string="Total Tax On Income", compute="_compute_taxable_amount")
    surcharge = fields.Monetary(string="Surcharge", compute="_compute_taxable_amount")
    health_education_cess = fields.Monetary(string="Health and Education Cess", compute="_compute_taxable_amount")
    total_tax_to_pay = fields.Monetary(string="Total Tax to be Paid", compute="_compute_taxable_amount")
    monthly_tds = fields.Monetary(string="Monthly TDS Payable", compute="_compute_monthly_tds")
    other_income_source = fields.Monetary(string="Other Source of Income")
    other_allowance = fields.Monetary(string="Other Allowance Details")
    # Below field is used to store manually added Total Income to ensure that while
    # modifying other_income_source & other_allowance values are reflected correctly
    # in the Total Income.
    manually_added_total_income = fields.Float()

    @api.depends("other_income_source", "other_allowance")
    def _compute_total_income(self):
        for record in self:
            if record.manually_added_total_income and record.total_income:
                record.total_income = record.manually_added_total_income + record.other_income_source + record.other_allowance
            else:
                record.total_income = (record.contract_id.wage * 12 if record.contract_id.wage else 0) + record.other_income_source + record.other_allowance

    def _inverse_total_income(self):
        for record in self:
            if record.total_income != (record.contract_id.wage * 12 if record.contract_id.wage else 0) + record.other_income_source + record.other_allowance:
                record.manually_added_total_income = record.total_income
                record.total_income += record.other_income_source + record.other_allowance

    @api.depends("total_income")
    def _compute_taxable_amount(self):
        """Computes the taxable amount, tax, rebate, surcharge, and total tax payable
            based on predefined tax slabs and thresholds.

            - Calculates `taxable_amount` after standard deductions.
            - Determines tax liability using progressive tax slabs.
            - Applies rebate if income is below the rebate threshold.
            - Computes surcharge for incomes exceeding the surcharge threshold.
            - Ensures surcharge does not exceed legal limits.
            - Adds health & education cess (4%) to derive total tax payable.
        """
        rule_parameter = self.env['hr.rule.parameter']
        tax_slabs = rule_parameter._get_parameter_from_code('l10n_in_tds_rate_chart_new_regime')
        tax_slabs_for_surcharge = rule_parameter._get_parameter_from_code('l10n_in_surcharge_rate')
        min_income_for_surcharge = rule_parameter._get_parameter_from_code('l10n_in_min_income_surcharge')
        min_income_for_rebate = rule_parameter._get_parameter_from_code('l10n_in_min_income_tax_rebate')

        for employee_declaration in self:
            employee_declaration.taxable_amount = max(employee_declaration.total_income - employee_declaration.standard_deduction, 0)

            tax = 0
            for rate, (lower, upper), fixed_tax in tax_slabs:
                if employee_declaration.taxable_amount >= lower and employee_declaration.taxable_amount <= upper:
                    taxable_amount_temp = employee_declaration.taxable_amount - lower
                    tax = fixed_tax + round(taxable_amount_temp * rate)
            employee_declaration.tax_on_taxable_amount = tax

            if employee_declaration.taxable_amount >= min_income_for_rebate:
                marginal_income = employee_declaration.taxable_amount - min_income_for_rebate
                employee_declaration.rebate = max(employee_declaration.tax_on_taxable_amount - marginal_income, 0)
            else:
                employee_declaration.rebate = employee_declaration.tax_on_taxable_amount
            employee_declaration.total_tax_on_income = employee_declaration.tax_on_taxable_amount - employee_declaration.rebate

            if employee_declaration.taxable_amount > min_income_for_surcharge:
                surcharge = 0
                for rate, amount in tax_slabs_for_surcharge:
                    if employee_declaration.taxable_amount <= float(amount[1]):
                        surcharge = employee_declaration.total_tax_on_income * rate
                        break

                max_tax_slabs = rule_parameter._get_parameter_from_code('l10n_in_max_surcharge_tax_rate')
                max_taxable_income, max_tax, max_surcharge = 0, 0, 0

                for income, tax, surcharge_rate in max_tax_slabs:
                    if employee_declaration.taxable_amount <= income:
                        break
                    else:
                        max_taxable_income, max_tax, max_surcharge = income, tax, surcharge_rate

                excess_income = employee_declaration.taxable_amount - max_taxable_income
                max_tax_with_surcharge = max_tax + max_surcharge
                total_tax_with_surcharge = employee_declaration.total_tax_on_income + surcharge
                excess_tax = total_tax_with_surcharge - max_tax_with_surcharge

                if excess_tax - excess_income > 0:
                    employee_declaration.surcharge = max_tax_with_surcharge + employee_declaration.taxable_amount - max_taxable_income - employee_declaration.total_tax_on_income
                else:
                    employee_declaration.surcharge = surcharge
            else:
                employee_declaration.surcharge = 0.0

            employee_declaration.health_education_cess = (employee_declaration.total_tax_on_income + employee_declaration.surcharge) * 0.04
            employee_declaration.total_tax_to_pay = employee_declaration.total_tax_on_income + employee_declaration.health_education_cess + employee_declaration.surcharge

    @api.depends("total_tax_to_pay")
    def _compute_monthly_tds(self):
        for record in self:
            record.monthly_tds = record.total_tax_to_pay / 12

    def action_tds_declaration_confirm(self):
        if self.state == "new":
            self.state = "verify"

    def action_tds_declaration_approve(self):
        if self.state in ("new", "verify"):
            self.state = "approve"

    def action_tds_declaration_cancel(self):
        if self.state not in ("cancel"):
            self.state = "cancel"

    def action_print_tds_declaration(self):
        return self.env.ref('hr_payroll_tds.action_report_tds_declaration').report_action(self.id)
