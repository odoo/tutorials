from odoo import fields, models


class fleetVehicleModeCategoryInherited(models.Model):
    _inherit = 'fleet.vehicle.model.category'

    max_weight = fields.Float()
    max_volume = fields.Float()

    def _compute_display_name(self):
        for record in self:
            computed_name = '{} ({}Kg, {}m3)'.format(record.name, record.max_weight, record.max_volume)
            record.display_name = computed_name
