from odoo import fields, models

class EstateSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    module_estate_account = fields.Boolean(
        string="Invoicing",
        config_parameter='estate.use_invoicing'
    )

    module_estate_auction_automation = fields.Boolean(
        string="Automated Auction",
        config_parameter='estate.use_auction_automation'
    )

    automated_auction = fields.Boolean(
        string="Enable Automated Auction",
        config_parameter="estate.automated_auction"
    )

    def set_values(self):
        """Save the setting and install the module if enabled."""
        super(EstateSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param(
            "estate.automated_auction", self.automated_auction
        )

        if self.automated_auction:
            module = self.env["ir.module.module"].search([("name", "=", "estate_auction")])
            if module and module.state != "installed":
                module.button_immediate_install()
