from odoo import fields, models


class EstatePropertyMaintenance(models.Model):
    _name = "estate.property.maintenance"
    _description = "this is model for estate property maintenance"

    actual_cost = fields.Float()
    description = fields.Text()
    estimate_cost = fields.Float()
    name = fields.Char(required=True)
    priority = fields.Selection(
        [
            ('high', "High"),
            ('medium', "Medium"),
            ('very_high', "Very High"),
        ],
    )
    property_id = fields.Many2one("estate.property", required=True)
    request_by_id = fields.Many2one("res.users")
    stage = fields.Selection(
        [
            ('assigned', "Assigned"),
            ('cancelled', "cancelled"),
            ('done', "done"),
            ('new', "New"),
        ],
    )
    technician_id = fields.Many2one("res.users")

    def action_assign_technician(self):
        for maintenance in self:
            maintenance.technician_id = self.env.user
            maintenance.stage = "assigned"
        return True

    def action_cancel(self):
        for maintenance in self:
            maintenance.stage = "cancelled"
        return True

    def action_done(self):
        for maintenance in self:
            maintenance.stage = "done"
        return True
