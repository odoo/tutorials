from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    estate_auction_enabled = fields.Boolean(string="Automated Auction", config_parameter='estate.auction_enabled')
    estate_account_enabled = fields.Boolean(string="Enabled Invoicing", config_parameter='estate.account_enabled')

    def write(self, vals):
        res = super().write(vals)

        estate_auction_module = self.env["ir.module.module"].search([("name", "=", "estate_auction")], limit=1)
        if estate_auction_module:
            if self.estate_auction_enabled and estate_auction_module.state in ["uninstalled"]:
                estate_auction_module.button_immediate_install()
            elif not self.estate_auction_enabled and estate_auction_module.state in ["installed"]:
                estate_auction_module.button_immediate_uninstall()

        estate_account_module = self.env["ir.module.module"].search([("name", "=", "estate_account")], limit=1)
        if estate_account_module:
            if self.estate_account_enabled and estate_account_module.state in ["uninstalled"]:
                estate_account_module.button_immediate_install()
            elif not self.estate_account_enabled and estate_account_module.state in ["installed"]:
                estate_account_module.button_immediate_uninstall()

        return res
