from odoo import models, fields, api


class AddEmiWizard(models.TransientModel):
    _name = 'installment.add.emi.wizard'
    _description = 'Add Emi Wizard'

    totalso_amount = fields.Float(string="Total Amount", readonly=True)
    down_payment = fields.Float(string="Down Payment", compute="_compute_values")
    remaining_amount = fields.Float(string="Remaining Amount", compute="_compute_values")
    remaining_amount2 = fields.Float(string="Remaining Amount2", compute="_compute_values")
    interest = fields.Float(string="Interest", compute="_compute_values")
    administrative_expense = fields.Float(string="Administrative Expense", compute="_compute_values")
    nof_installment = fields.Integer(string="No. of Monthly Installment", compute="_compute_values")
    installment_amount = fields.Float(string="Installment Amount", compute="_compute_values")

    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        defaults['totalso_amount'] = self.env['sale.order'].browse(self.env.context.get('active_id')).amount_total
        return defaults

    @api.depends("totalso_amount")
    def _compute_values(self):
        for rec in self:
            down_payment_percent = self.env['ir.config_parameter'].get_param('installment.down_payment_percentage')
            x = float(rec.totalso_amount) * float(down_payment_percent)
            rec.down_payment = x / 100
            rec.remaining_amount = rec.totalso_amount - rec.down_payment
            administrative_expense_percent = self.env['ir.config_parameter'].get_param('installment.administrative_expense_percentage')
            y = float(rec.remaining_amount) * float(administrative_expense_percent)
            rec.administrative_expense = y / 100
            rec.remaining_amount2 = rec.remaining_amount + rec.administrative_expense
            annual_rate_percent = self.env['ir.config_parameter'].get_param('installment.annual_rate_percentage')
            z = float(rec.remaining_amount2) * float(annual_rate_percent)
            rec.interest = z / 100
            nof_install = float(self.env['ir.config_parameter'].get_param('installment.max_duration'))
            rec.nof_installment = nof_install * 12
            final_amount = rec.remaining_amount2 + rec.interest
            rec.installment_amount = final_amount / rec.nof_installment

    def action_add_emi(self):
        move_vals = [{
            'product_id': self.env.ref('installment.product_1').id,
            'order_id': self.env.context.get('active_id'),
            'price_unit': self.installment_amount,
            'product_uom_qty': 1
        },
        {
            'product_id': self.env.ref('installment.product_2').id,
            'order_id': self.env.context.get('active_id'),
            'product_uom_qty': 4,
            'price_unit': -self.installment_amount,
        }]
        self.env['sale.order.line'].create(move_vals)
