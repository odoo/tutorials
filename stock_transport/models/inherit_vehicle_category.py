from odoo import api, fields, models


class FleetVehicleModelCategory(models.Model):
    _inherit = 'fleet.vehicle.model.category'

    max_weight = fields.Float(string='Max Weight (kg)')
    max_volume = fields.Float(string='Max Volume (m³)')
    display_name = fields.Char(string='Display Name', compute='_compute_display_name', store=False)

    @api.depends('name', 'max_weight', 'max_volume')
    def _compute_display_name(self):
        for record in self:
            weight_str = f"{record.max_weight}kg" if record.max_weight else "N/A"
            volume_str = f"{record.max_volume}m³" if record.max_volume else "N/A"
            record.display_name = f"{record.name} ({weight_str}, {volume_str})"
