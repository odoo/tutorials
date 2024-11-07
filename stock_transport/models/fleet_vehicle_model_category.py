from odoo import fields, models


class FleetVehicleModeCategory(models.Model):
    _inherit = 'fleet.vehicle.model.category'

    max_weight = fields.Float()
    max_volume = fields.Float()

    def _compute_display_name(self):
        for record in self:
            computed_name = f"{record.name}: {record.max_weight}Kg, {record.max_volume}m3"
            record.display_name = computed_name
