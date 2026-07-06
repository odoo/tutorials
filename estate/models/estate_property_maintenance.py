from datetime import timedelta
from odoo import fields, models


class EstatePropertyMaintenance(models.Model):
    _name = "estate.property.maintenance"
    _description = "Real Estate Property Maintenance"

    title = fields.Char(required=True)
    problem = fields.Char()
    technician_id = fields.Many2one(
        "res.partner",
        string="Technician",
    )
    requested_by = fields.Many2one(
        "res.users",
        string="Requested By",
        default=lambda self: self.env.user,
    )
    estimated_cost = fields.Float()
    actual_cost = fields.Float()
    property_id = fields.Many2one(
        "estate.property",
        required=True,
    )
    priority = fields.Selection(
        [
            ("high", "High"),
            ("medium", "Medium"),
            ("low", "Low"),
        ]
    )
    assigned_date = fields.Date(
        default=lambda self: fields.Datetime.now()
    )
    completion_date = fields.Date()
    state = fields.Selection(
        [
            ("new", "New"),
            ("started", "Started"),
            ("in_progress", "In Progress"),
            ("completed", "Completed"),
        ],
        string="Status",
        default="new",
        required=True,
    )
    # When state is completed, complition date will be set automatically
    def write(self, vals):
        if "state" in vals:
            if vals["state"] == "completed":
                vals["completion_date"] = fields.Date.today()
            else:
                vals["completion_date"] = False
        return super().write(vals)
