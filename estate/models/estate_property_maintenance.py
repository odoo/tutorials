from odoo import api, fields, models


class EstatePropertyMaintenance(models.Model):
    _name = "estate.property.maintenance"
    _description = "Estate maintenance"

    name = fields.Char()
    description = fields.Text(required=True)

    property_id = fields.Many2one(
        "estate.property",
        string="Property",
        required=True
        )
    technician_id = fields.Many2one(
        "res.users",
        string="technician"
    )
    state = fields.Selection(
        [
            ('new', "New"),
            ('assigned', "assigned"),
            ('in_progress', "In progress"),
            ('done', "done"),
            ('cancel', "cancel"),
        ],
    )
    estimated_cost = fields.Float(required=True)
    actual_cost = fields.Float(readonly=True)

    @api.onchange("technician_id")
    def _onchange_technician(self):
        if self.technician_id and self.state == "new":
            self.state = "assigned"

    def action_stop(self):
        for record in self:
            if record.state == "in_progress":
                record.state = "done"

    def action_start(self):
        for record in self:
            if record.state == "assigned":
                record.state = "in_progress"

    def action_cancel(self):
        for record in self:
            record.state = "cancel"
