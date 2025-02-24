# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    estate_property_id = fields.Many2one(comodel_name='estate.property', string="Estate Property", store=True)

    def action_open_estate_property(self):
        return {
            'name': _("Open estate property of this invoice"),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_id': 'estate_property_view_form',
            'views': [[False, 'form']],
            'res_model': 'estate.property',
            'res_id': self.estate_property_id.id,
        }
