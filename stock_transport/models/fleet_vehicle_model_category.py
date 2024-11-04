from odoo import fields, models


class FleetVehicleModelCategory(models.Model):
    _inherit = 'fleet.vehicle.model.category'

    max_weight = fields.Float(default=0, string="Max Weight (kg)")
    max_volume = fields.Float(default=0, string="Max Volume (m³)")

    def _compute_display_name(self):
        res = super()._compute_display_name()
        for record in self:
            record.display_name = f"{record.name} ({record.max_weight}kg, {record.max_volume}m³)"
        return res
