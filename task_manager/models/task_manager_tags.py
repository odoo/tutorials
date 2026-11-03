from odoo import fields, models


class TaskManagerTags(models.Model):
    _name = "task.manager.tags"
    _description = "Tags for Tasks"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer()

    _check_unique_tag = models.Constraint(
        "UNIQUE(name)",
        "A property tag name must be unique",
    )
