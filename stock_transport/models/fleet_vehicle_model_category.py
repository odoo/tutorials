from odoo import fields, models


class FleetVehicleModelCategory(models.Model):
    _inherit = 'fleet.vehicle.model.category'

    max_weight = fields.Float()
    max_volume = fields.Float()

    def _compute_display_name(self):
        for record in self:
            record.display_name = record.name + ' (' + str(record.max_weight) + ' kg, ' + str(record.max_volume) + ' m3)'
