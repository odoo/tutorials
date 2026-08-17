from odoo import fields, models


class SettingsEstate(models.Model):
    _name = "settings.estate"
    _description = "Estate Management Settings"

    name = fields.Char(
        string="Setting Name",
        required=True,
    )

    start_date = fields.Datetime(
        string="Start Date",
        required=True,
    )

    end_date = fields.Datetime(
        string="End Date",
    )

    active = fields.Boolean(
        string="Active",
        default=True,
    )

    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("active", "Active"),
            ("closed", "Closed"),
        ],
        string="Status",
        default="draft",
    )

    budget = fields.Float(
        string="Budget",
    )

    property_count = fields.Integer(
        string="Number of Properties",
    )

    notes = fields.Text(
        string="Notes",
    )
