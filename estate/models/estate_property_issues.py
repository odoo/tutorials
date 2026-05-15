from datetime import timedelta

from odoo import api, fields, models

AVAILABLE_PRIORITIES = [
    ('1', 'Low'),
    ('2', 'Medium'),
    ('3', 'High'),
]


class EstatePropertyIssues(models.Model):
    _name = 'estate.property.issue'
    _description = "Raise and Manage issues in properties"

    name = fields.Char(required=True)
    property_id = fields.Many2one('estate.property', required=True)
    reported_by = fields.Many2one('res.partner')
    assigned_to = fields.Many2one('res.users')
    issue_type = fields.Selection(
        selection=[
            ('plumbing', 'Plumbing'),
            ('electrical', 'Electrical'),
            ('structural', 'Structural'),
            ('other', 'other'),
        ],
        required=True
    )
    state = fields.Selection(
        string="Status",
        selection=[
            ("new", "New"),
            ("in_progress", "In progress"),
            ("resolved", "Resolved"),
            ("cancelled", "Cancelled")
        ],
        default="new",
    )
    priority = fields.Selection(
        AVAILABLE_PRIORITIES, compute="_compute_priority"
    )
    resolved_date = fields.Date()
    description = fields.Text()
    is_overdue = fields.Boolean(compute="_compute_is_overdue", default=False)

    @api.depends('issue_type')
    def _compute_priority(self):
        for record in self:
            if record.issue_type not in ('electrical', 'structural'):
                record.priority = '1'
            if record.issue_type == 'electrical':
                record.priority = '2'
            if record.issue_type == 'structural':
                record.priority = '3'

    @api.depends('create_date', 'priority', 'resolved_date')
    def _compute_is_overdue(self):
        priority_days = {
            '3': 2,
            '2': 5,
            '1': 10,
        }

        for record in self:
            start_date = record.create_date.date() if record.create_date else fields.Date.today()
            resolve_date = record.resolved_date or fields.Date.today()
            limit_days = priority_days.get(record.priority)

            if (resolve_date - start_date) > timedelta(days=limit_days):
                record.is_overdue = True
            else:
                record.is_overdue = False

    @api.onchange('assigned_to')
    def _check_state(self):
        for record in self:
            if record.assigned_to and record.state == "new":
                record.state = "in_progress"

    def action_set_resolved(self):
        self.state = 'resolved'
        if not self.resolved_date:
            self.resolved_date = fields.Date.today()
        return True

    def action_set_cancelled(self):
        self.state = 'cancelled'
        return True
