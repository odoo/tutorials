from odoo import fields, models


class PropertyMaintenance(models.Model):
    _name = "property.maintenance"
    _description = "Property under repair"

    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    property_id = fields.Many2one("estate.property", required=True)
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
        default="0",
    )
    user_id = fields.Many2one(
        "res.users",
        string="Assigned to",
    )
    estimated_cost = fields.Float()
    actual_cost = fields.Float()
    state = fields.Selection(
        [
            ('new_request', "New Request"),
            ('assign', "Assign"),
            ('work_in_progress', "Work In Progress"),
            ('done', "Done"),
        ],
        default='new_request',
    )
