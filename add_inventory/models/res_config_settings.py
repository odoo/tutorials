from odoo import models, fields, api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    group_stock_multi_locations = fields.Boolean(
        string="Storage Locations",
        implied_group="stock.group_stock_multi_locations",
        help="Store products in specific locations of your warehouse (e.g., bins, racks) and track inventory accordingly.",
        config_parameter="stock.storage_locations"
    )

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        config_value = self.env['ir.config_parameter'].sudo().get_param('stock.storage_locations')
        # You can process the value if needed before returning it
        res.update({
            'group_stock_multi_locations': config_value in ['True', 'true', '1'],
        })
        return res
    
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param(
            'stock.storage_locations', self.group_stock_multi_locations
        )
