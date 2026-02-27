from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyMaintenance(models.Model):
    _name = "estate.property.maintenance"
    _description = "Estate Property Maintenance"

    problem = fields.Char()

    property_id = fields.Many2one("estate.property", string="Property", required=True)
    technician_id = fields.Many2one("res.users", string="technician")
    state = fields.Selection(
        [
            ("new", "New"),
            ("assigned", "assigned"),
            ("in_progress", "In progress"),
            ("done", "done"),
            ("cancel", "cancel"),
        ],
        default="new",
    )
    estimated_cost = fields.Float(required=True)
    actual_cost = fields.Float(string="Actual Cost")

    @api.onchange("technician_id")
    def _onchange_technician(self):
        if self.technician_id and self.state == "new":
            self.state = "assigned"

    def action_stop(self):
        for record in self:
            if record.state == "cancel":
                raise UserError("cancelled tasks cannot be done !!")
            if record.state == "in_progress":
                record.state = "done"

    def action_start(self):
        for record in self:
            if not record.estimated_cost:
                raise UserError("estimated cost should be given to start")
            if record.state == "assigned":
                record.state = "in_progress"

    def action_cancel(self):
        for record in self:
            record.state = "cancel"
