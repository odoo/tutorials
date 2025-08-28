from odoo import api, fields, models


class AccountMoveCustomDutyLine(models.TransientModel):
    _name = "account.move.custom.duty.line"
    _description = "Account Move Custom Duty Line"
    
    _sql_constraints = [
        ("zero_or_positive_custom_duty_with_added_charges", "CHECK(custom_duty_with_added_charges >= 0)", "Custom duty with added charges must be either 0 or positive.")
    ]
    
    account_move_line_id = fields.Many2one(comodel_name="account.move.line")
    account_move_custom_duty_id = fields.Many2one(comodel_name="account.move.custom.duty")
    currency_id = fields.Many2one(related="account_move_custom_duty_id.currency_id")
    custom_duty_with_added_charges = fields.Monetary(string="Custom Duty + Additional Charges", currency_field="currency_id")
    tax_ids = fields.Many2many(comodel_name="account.tax", string="Taxes", domain=[("type_tax_use", "=", "purchase")])
    
    # computed fields
    assessable_value = fields.Monetary(string="Assessable Value", currency_field="currency_id", compute="_compute_assessable_value")
    taxable_amount = fields.Monetary(string="Taxable Amount", currency_field="currency_id", compute="_compute_taxable_amount")
    tax_amount = fields.Monetary(string="Tax Amount", compute="_compute_tax_amount")
    
    @api.depends("account_move_custom_duty_id.custom_currency_rate")
    def _compute_assessable_value(self):
        for record in self:
            record.assessable_value = record.account_move_line_id.price_subtotal * record.account_move_custom_duty_id.custom_currency_rate
    
    @api.depends("assessable_value", "custom_duty_with_added_charges")
    def _compute_taxable_amount(self):
        for record in self:
            record.taxable_amount = record.assessable_value + record.custom_duty_with_added_charges

    @api.depends("taxable_amount", "tax_ids")
    def _compute_tax_amount(self):
        for record in self:
            if not record.taxable_amount or not record.tax_ids:
                record.tax_amount = 0
                continue
            
            taxes_result = record.tax_ids.compute_all(record.taxable_amount, currency=record.account_move_line_id.company_id.currency_id)
            record.tax_amount = taxes_result["total_included"] - taxes_result["total_excluded"]
