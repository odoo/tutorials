from odoo import models, fields
from odoo.exceptions import UserError


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    deposit_product_id = fields.Many2one(
        'product.product',
        string='Deposit Product',
        config_parameter='rental_deposit.deposit_product_id',
        domain="[('type', '=', 'service'), ('rent_ok', '=', False)]",
        help="This product will be used for deposit lines on rental orders."
    )

    def action_set_deposit(self):
        """Set the deposit product configuration."""
        if self.deposit_product_id:
            self.env['ir.config_parameter'].set_param('rental_deposit.deposit_product_id', self.deposit_product_id.id)
            return {
                'type': 'ir.actions.client',
                'tag': 'reload',
            }
        else:
            raise UserError("Please select a deposit product before setting it.")
