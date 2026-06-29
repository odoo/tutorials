from datetime import timedelta

from odoo import models, fields, api


class EstatePropertyIssue(models.Model):
    _name = "estate.property.issue"
    _description = "Property Issue"

    name = fields.Char(string="Issue Title", required=True)
    property_id = fields.Many2one(
        "estate.property",
        string="Property",
        required=True
    )
    partner_id = fields.Many2one(
        "res.partner",
        string="Reported By"
    )
    salesman_id = fields.Many2one(
        "res.users",
        string="Assign To"
    )
    issue_type = fields.Selection(
        [
            ('plumbing', 'Plumbing'),
            ('electrical', 'Electrical'),
            ('structural', 'Structural'),
            ('other', 'Other')
        ],
        string="Issue Type",
        required=True
    )
    state = fields.Selection(
        [
            ('new', 'New'),
            ('in_progress', 'In Progress'),
            ('resolved', 'Resolved'),
            ('cancel', 'Cancelled')
        ],
        default='new',
        string="Status"
    )
    priority = fields.Selection(
        [
            ('low', 'Low'),
            ('medium', 'Medium'),
            ('high', 'High')
        ],
        string="Priority",
        compute="_compute_priority",
        store=True
    )
    is_overdue = fields.Boolean(
        compute="_compute_is_overdue"
    )
    reported_date = fields.Date(
        string="Reported Date",
        default=fields.Date.today
    )
    resolved_date = fields.Date(string="Resolved Date", readonly=True)
    description = fields.Text(string="Description")
    end_date = fields.Date(compute="_compute_end_date")

    @api.depends("issue_type")
    def _compute_priority(self):
        for record in self:
            if record.issue_type == 'structural':
                record.priority = 'high'
            elif record.issue_type == 'electrical':
                record.priority = 'medium'
            else:
                record.priority = 'low'

    @api.onchange("salesman_id")
    def _onchange_salesman(self):
        for record in self:
            if record.salesman_id:
                record.state = 'in_progress'

    @api.depends("priority", "reported_date")
    def _compute_end_date(self):
        for record in self:
            if record.reported_date:
                if record.priority == 'high':
                    record.end_date = record.reported_date + timedelta(days=2)
                elif record.priority == 'medium':
                    record.end_date = record.reported_date + timedelta(days=5)
                else:
                    record.end_date = record.reported_date + timedelta(days=10)

    @api.depends("state", "end_date")
    def _compute_is_overdue(self):
        for record in self:
            if record.state != 'resolved' and fields.Date.today() > record.end_date:
                record.is_overdue = True
            else:
                record.is_overdue = False

    def action_resolved(self):
        for record in self:
            record.state = 'resolved'
            record.resolved_date = fields.Date.today()

    def action_cancel(self):
        for record in self:
            record.state = 'cancel'
