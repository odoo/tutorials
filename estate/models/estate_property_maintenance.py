from odoo import fields, models


class EstatePropertyMaintenance(models.Model):
    _name = "estate.property.maintenance"
    _description = "this is model for estate property maintenance"
    name = fields.Char()
    property_id = fields.Many2one('estate.property')
    request_by_id = fields.Many2one("res.users")
    description = fields.Text()
    priority = fields.Selection(
        [('high', "High"), ('very_high', "Very High"), ('medium', "Medium")]
    )
    technician_id = fields.Many2one('res.users')
    estimate_cost = fields.Float()
    actual_cost = fields.Float()
    stage = fields.Selection(
        [
            ('new', "New"),
            ('assigned', "Assigned"),
            ('done', "done"),
            ('cancelled', "cancelled"),
        ]
    )

    def action_assign_technician(self):
        for maintenance in self:
            maintenance.technician_id = self.env.user
            maintenance.stage = "assigned"
        return True

    def action_done(self):
        for maintenance in self:
            maintenance.stage = "done"
        return True

    def action_cancel(self):
        for maintenance in self:
            maintenance.stage = "cancelled"
        return True
