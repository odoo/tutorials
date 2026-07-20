from odoo import fields, models


class EstateProperty(models.Model):
    _name = "maintenance.property"
    _description = "maintenance property"

    title = fields.Char()
    prop_id = fields.Many2one('estate.property', required=True)
    description = fields.Char()
    priority = fields.Selection(
        [
            ("low", "Low"),
            ("normal", "Normal"),
            ("high", "High"),
        ],
    )
    stage = fields.Selection(
        [
            ("new", "New"),
            ("assigned", "Assigned"),
            ("progress", "In Progress"),
            ("complete", "Complete"),
        ],
        string="Stage",
        default="new"
    )
    assigned = fields.Many2one("res.users", string="Assigned To", default=lambda self: self.env.user)
    estimated_cost = fields.Float(string="Estimated Cost")
    actual_cost = fields.Float(string="Actual Cost")
    date = fields.Date(default=fields.Date.today())
    cost = fields.Float()

    def mark_assigned(self):
        for maintenance in self:
            maintenance.stage = "assigned"

    def mark_progress(self):
        for maintenance in self:
            maintenance.stage = "progress"

    def mark_complete(self):
        for maintenance in self:
            maintenance.stage = "complete"
