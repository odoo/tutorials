from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    deposit_id = fields.Many2many(
        'product.product', string="Deposit Product",
        help="This product will be used to add deposit in the Rental Order.", related="company_id.deposit_id",
        readonly=False)
