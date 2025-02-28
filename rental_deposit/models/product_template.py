from odoo import fields, models, api

class ProductTemplate(models.Model):
    _inherit = "product.template"

    require_deposit = fields.Boolean("Require Deposit" , default = False, store = True)
    amount = fields.Float("Amount" , default = 0)
    deposit_management_enabled = fields.Boolean(
        compute='_compute_deposit_management', string='Deposit Management Enabled'
    )

    @api.model
    def _compute_deposit_management(self):
        deposit_management = self.env['ir.config_parameter'].get_param('sale_renting.deposit_management')
        self.deposit_management_enabled = bool(deposit_management)
        if deposit_management == False:
             self.require_deposit = False
        
    @api.onchange('require_deposit')
    def require_deposit_value_change(self):
        self.amount = 0
