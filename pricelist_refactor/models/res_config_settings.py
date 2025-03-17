from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    module_sale_subscription = fields.Boolean("Sale Subscription")
    group_product_pricelist = fields.Boolean("Pricelists", default=True)

    @api.constrains('group_product_pricelist')
    def _check_pricelist_requirement(self):
        """Prevent disabling pricelists if Sale Subscription is installed"""
        for config in self:
            if not config.group_product_pricelist and self.env['ir.module.module'].search_count([
                ('name', '=', 'sale_subscription'),
                ('state', '=', 'installed')
            ]):
                raise UserError(_("Pricelists are required for Sale Subscription. You cannot disable them."))
