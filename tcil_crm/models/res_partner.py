# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        if self.env.context.get('default_parent_id', False):
            partner = self.env['res.partner'].browse(self.env.context.get('default_parent_id')).exists()
            defaults.update({
                'street': partner.street,
                'street2': partner.street2,
                'city': partner.city,
                'state_id': partner.state_id.id,
                'zip': partner.zip,
                'country_id': partner.country_id.id,
                'user_id': partner.user_id.id,
            })
        return defaults

    is_selected_line = fields.Boolean(string="Selected Address Line", copy=False)
