from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"
    
    estate_account = fields.Boolean(string="Auto Install Estate Account", config_parameter="estate.account_estate")
    estate_auction = fields.Boolean(string="Auto Install Estate Auction", config_parameter="estate.auction_estate")
    
    def execute(self):
        res = super().execute()

        modules_to_manage = {
            "estate_account": self.estate_account,
            "estate_auction": self.estate_auction,
        }

        for module_name, should_be_installed in modules_to_manage.items():
            module = self.env["ir.module.module"].search([("name", "=", module_name)], limit=1)

            if module and module.state != "installed" and should_be_installed:
                module.button_immediate_install()
            elif module and module.state == "installed" and not should_be_installed:
                module.button_immediate_uninstall()

        return res
