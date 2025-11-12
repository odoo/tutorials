from odoo import api, models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    automated_auction = fields.Boolean(
        string="Automated Auction",
        config_parameter='estate.automated_auction'
    )

    @api.model
    def set_values(self):
        res = super().set_values()
        install_module = self.env['ir.module.module'].search([('name', '=', 'estate_auction')])
        if self.automated_auction and install_module.state != 'installed':
            install_module.button_immediate_install()
        return res
