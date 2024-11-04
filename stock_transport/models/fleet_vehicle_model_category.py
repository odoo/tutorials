# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api


class FleetVehicleModelCategory(models.Model):
    _inherit = 'fleet.vehicle.model.category'
    max_weight = fields.Float()
    max_volume = fields.Float()

    @api.depends('max_weight', 'max_volume')
    def _compute_display_name(self):
        for record in self:
            name = f"{record.name} ({record.max_weight}kg, {record.max_volume}m³)"
            record.display_name = name
