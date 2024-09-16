from odoo import models, fields, api


class ActionOpenEmiWizard(models.TransientModel):
    _name = 'action.open.emi.wizard'
    _description = 'Installment Settings'

    total_so_amount = fields.Float(string="Total SO Amount")
    down_payment = fields.Float(string="Down Payment", compute="_compute_values")
    remaining_amount = fields.Float(string="Remaining Amount", compute="_compute_values")
    remaining_amount2 = fields.Float(string="Remaining Amount", compute="_compute_values")
    interest = fields.Float(string="Interest", compute="_compute_values")
    admin_expence = fields.Float(string="Administrative Expense", compute="_compute_values")
    num_installments = fields.Integer(string="Number of Monthly Installments", compute="_compute_values")
    installment_amount = fields.Float(string="Installment Amount", compute="_compute_values")

    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        defaults['total_so_amount'] = self.env['sale.order'].browse(self.env.context.get('active_id')).amount_total
        return defaults

    @api.depends("total_so_amount")
    def _compute_values(self):
        for rec in self:
            down_payment_percent = self.env['ir.config_parameter'].get_param('installments.down_payment_perc')
            x = float(rec.total_so_amount) * float(down_payment_percent)
            rec.down_payment = x / 100
            rec.remaining_amount = rec.total_so_amount - rec.down_payment
            administrative_expense_percent = self.env['ir.config_parameter'].get_param('installments.admin_exp_perc')
            y = float(rec.remaining_amount) * float(administrative_expense_percent)
            rec.admin_expence = y / 100
            rec.remaining_amount2 = rec.remaining_amount + rec.admin_expence
            annual_rate_percent = self.env['ir.config_parameter'].get_param('installments.annual_rate')
            z = float(rec.remaining_amount2) * float(annual_rate_percent)
            rec.interest = z / 100
            nof_install = float(self.env['ir.config_parameter'].get_param('installments.max_duration'))
            rec.num_installments = nof_install * 12
            final_amount = rec.remaining_amount2 + rec.interest
            rec.installment_amount = final_amount / rec.num_installments

    def add_installment(self):
        move_vals = [{
            'product_id': self.env.ref('installments.installment_product').id,
            'order_id': self.env.context.get('active_id'),
            'name': "Installment",
            'product_uom_qty' : 1,
            'price_unit': self.installment_amount
        }, {
            'product_id': self.env.ref('installments.emi_product').id,
            'order_id': self.env.context.get('active_id'),
            'name': "Monthly EMI",
            'product_uom_qty' : 4,
            'price_unit': -(self.installment_amount)
        }]
        self.env['sale.order.line'].create(move_vals)
