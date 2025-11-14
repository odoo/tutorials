from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    requires_deposit = fields.Boolean(string="Requires Deposit")
    deposit_amount = fields.Monetary(
        string="Deposit Amount",
        currency_field='currency_id',
        help="Deposit amount required for one unit of this product."
    )

    @api.onchange('requires_deposit')
    def _onchange_requires_deposit(self):
        if self.requires_deposit:
            param_obj = self.env['ir.config_parameter'].sudo()
            deposit_product_id = param_obj.get_param('rental_deposit.deposit_product_id')
            if deposit_product_id:
                deposit_product = self.env['product.product'].browse(int(deposit_product_id))
                if deposit_product:
                    self.deposit_amount = deposit_product.list_price
                else:
                    self.deposit_amount = 0.0
            else:
                self.deposit_amount = 0.0
        else:
            self.deposit_amount = 0.0


class ProductProduct(models.Model):
    _inherit = 'product.product'

    requires_deposit = fields.Boolean(related='product_tmpl_id.requires_deposit', readonly=False)
    deposit_amount = fields.Monetary(related='product_tmpl_id.deposit_amount', currency_field='currency_id', readonly=False)
