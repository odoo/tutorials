from odoo import api, fields, models


class FleetVehicleModelCategory(models.Model):
    _inherit = 'fleet.vehicle.model.category'

    max_weight = fields.Float(default=0, string="Max Weight (kg)", groups="stock_transport.group_stock_transport_admin")
    max_volume = fields.Float(default=0, string="Max Volume (m³)", groups="stock_transport.group_stock_transport_admin")

    @api.depends('max_weight', 'max_volume')
    def _compute_display_name(self):
        res = super()._compute_display_name()
        for record in self:
            record.display_name = f"{record.name} ({record.max_weight}kg, {record.max_volume}m³)"
        return res
