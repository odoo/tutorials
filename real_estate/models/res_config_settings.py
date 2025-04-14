from odoo import fields, models, api


class EstateSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    module_estate_account = fields.Boolean(
        string="Invoicing",
        config_parameter='real_estate.use_invoicing'
    )

    module_estate_auction_automation = fields.Boolean(
        string="Automated Auction",
        config_parameter='real_estate.use_auction_automation'
    )

    automated_auction = fields.Boolean(
        string="Enable Automated Auction",
        config_parameter="real_estate.automated_auction"
    )

    @api.model
    def get_values(self):
        res = super().get_values()
        res.update({
            'automated_auction': self.env['ir.config_parameter'].sudo().get_param(
                'real_estate.automated_auction', default=False
            ),
        })
        return res

    def set_values(self):
        super().set_values()
        self.env['ir.config_parameter'].sudo().set_param(
            "real_estate.automated_auction", self.automated_auction
        )

        if self.automated_auction:
            module = self.env["ir.module.module"].search([("name", "=", "estate_auction")], limit=1)
            if module and module.state not in ("installed", "to install"):
                module.button_immediate_install()
