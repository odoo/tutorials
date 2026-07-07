from odoo import fields, models


class PropertyMaintenance(models.Model):
    _name = "property.maintenance"
    _description = "proeprty under repair"

    name = fields.Char(string="Title", required=True)
    description = fields.Text(string="Description")
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    partner_id = fields.Many2one(
        "res.partner",
        string="Requested by",
        copy=False,
        default=lambda self: self.env.user.partner_id,
    )
    date = fields.Date(string="Date", default=fields.Date.context_today)
    priority = fields.Selection(
        [
            ("0", "Normal"),
            ("1", "Low"),
            ("2", "High"),
            ("3", "Very High"),
        ],
        string="Priority",
        default="0",
    )
    user_id = fields.Many2one(
        "res.users",
        string="Assigned to",
    )
    estimated_cost = fields.Float(string="Estimated cost")
    actual_cost = fields.Float(string="Actual cost")
    state = fields.Selection(
        [
            ("new_request", "New Request"),
            ("assign", "Assign"),
            ("work_in_progress", "Work In Progress"),
            ("done", "Done"),
        ],
        default="new_request",
    )
