from odoo import fields, models


class FleetVehicleModelCategory(models.Model):
    _inherit = 'fleet.vehicle.model.category'
    
    max_weight = fields.Float(string="Max Weight(kg)")
    max_volume = fields.Float(string="Max Volume(m³)")

    def _compute_display_name(self):
        for record in self:
            base_name = record.name
            additional_info = f" ({record.max_weight} kg, {record.max_volume} m³)" if record.max_weight or record.max_volume else ""
            record.display_name = f"{base_name}{additional_info}"
