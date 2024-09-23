from odoo import models, fields, api


class AddEmiButtonWizard(models.TransientModel):

    _name = "add.emi.button.wizard"
    _description = "Add Emi Button Wizard"

    total_sale_amount = fields.Float(
        string="Total sale Amount", readonly=True)
    down_payment = fields.Float(compute="_compute_values")
    remaining_amount = fields.Float(compute="_compute_values")
    interest = fields.Float(compute='_compute_values')
    number_of_monthly_installement = fields.Integer(compute='_compute_values')
    installement_amount = fields.Float(readonly=True)
    admin_expense = fields.Float(compute='_compute_values')
    remaining_amount_2 = fields.Float(compute='_compute_values')

    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        defaults['total_sale_amount'] = self.env['sale.order'].browse(
            self.env.context.get('active_id')).amount_total
        return defaults

    @api.depends("total_sale_amount")
    def _compute_values(self):
        for rec in self:
            # fetching down_payment_percent from setting and calulating down payment
            down_payment_percent = self.env['ir.config_parameter'].get_param(
                'installement.down_payment_percentage')
            x = float(rec.total_sale_amount) * float(down_payment_percent)
            rec.down_payment = x / 100

            # calculating remaining amount
            rec.remaining_amount = rec.total_sale_amount - rec.down_payment

            # fetching administrative_expenses_percentage from setting and calulating admin expense
            administrative_expenses_percentage = self.env['ir.config_parameter'].get_param(
                'installement.administrative_expenses_percentage')
            y = float(rec.remaining_amount) * \
                float(administrative_expenses_percentage)
            rec.admin_expense = y / 100

            # toal remaining amount
            rec.remaining_amount_2 = rec.remaining_amount + rec.admin_expense

            # fetching annual rate percentage from setting and calulating interest
            annual_rate_percentage = self.env['ir.config_parameter'].get_param(
                'installement.annual_rate_percentage')
            z = float(rec.remaining_amount_2) * float(annual_rate_percentage)
            rec.interest = z / 100

            max_dur = float(self.env['ir.config_parameter'].get_param(
                'installement.max_duration'))
            rec.number_of_monthly_installement = float(max_dur) * 12

            # calculating installement amount
            rec.installement_amount = (
                rec.remaining_amount_2 + rec.interest) / rec.number_of_monthly_installement

    def add_installment(self):
        sale_order = self.env['sale.order'].browse(
            self.env.context.get('active_id'))
        installment_product = self.env.ref('installement.installment_product')
        monthly_emi_product = self.env.ref('installement.monthly_emi_product')
        if sale_order:
            self.env['sale.order.line'].create([
                {
                    'order_id': sale_order.id,
                    'product_id': installment_product.id,
                    'name': 'Installment',
                    'product_uom_qty': 1,
                    'price_unit': self.installement_amount,
                },
                {
                    'order_id': sale_order.id,
                    'product_id': monthly_emi_product.id,
                    'name': 'Monthly EMI',
                    'product_uom_qty': 1,
                    'price_unit': self.installement_amount,
                }
            ])

            self.env['sale.order'].browse(
                self.env.context.get('active_id')).is_installable = True
            self.env['sale.order'].browse(self.env.context.get(
                'active_id')).installement_amount = self.installement_amount
