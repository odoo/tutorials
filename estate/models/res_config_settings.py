from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    auto_auction = fields.Boolean(string="Auto Install Auction", config_parameter="estate.auto_auction")
    auto_account_estate = fields.Boolean(string="Auto Install Account Estate", config_parameter="estate.auto_account_estate")

    def execute(self):
        """Override execute to install/uninstall module based on checkbox state."""
        res = super().execute()
        module_auction = self.env['ir.module.module'].search([('name', '=', 'estate_auction')])
        module_account_estate = self.env['ir.module.module'].search([('name', '=', 'estate_account')])

        if self.auto_auction:
            if module_auction and module_auction.state != 'installed':
                module_auction.button_immediate_install()
        else:
            if module_auction and module_auction.state == 'installed':
                module_auction.button_immediate_uninstall()

        if self.auto_account_estate:
            if module_account_estate and module_account_estate.state != 'installed':
                module_account_estate.button_immediate_install()
        else:
            if module_account_estate and module_account_estate.state == 'installed':
                module_account_estate.button_immediate_uninstall()

        return res
