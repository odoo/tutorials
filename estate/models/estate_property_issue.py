from datetime import timedelta
from odoo import api, fields, models


class EstatePropertyIssue(models.Model):
    _name = "estate.property.issue"
    _description = "Property Issue"

    name = fields.Char(required=True)
    property_id = fields.Many2one('estate.property', required=True)

    buyer_id = fields.Many2one(
        "res.partner",
        string="Reported By",
        copy=False,
    )

    salesman_id = fields.Many2one(
        "res.users",
        string="Assigned By",
    )

    issue_type = fields.Selection(
        selection=[
            ('plumbing', "Plumbing"),
            ('electrical', "Electrical"),
            ('structural', "Structural"),
            ('others', "Others"),
        ],
        required=True,
    )

    staty = fields.Selection(
        selection=[
            ('new', "New"),
            ('in_progress', "In Progress"),
            ('resolved', "Resolved"),
            ('canceled', "Canceled"),
        ],
        default='new'
    )

    priority = fields.Selection(
        selection=[
            ('low', "Low"),
            ('medium', "Medium"),
            ('high', "High"),
        ],
        compute="_compute_priority",
        store=True,
        readonly=True,
    )

    resolved_date = fields.Datetime()
    description_issue = fields.Text()

    is_overdue = fields.Boolean(
        compute="_compute_is_overdue",
        store=True,
        string="Overdue",
    )

    @api.depends("issue_type")
    def _compute_priority(self):
        for rec in self:
            if rec.issue_type in ('others', 'plumbing'):
                rec.priority = 'low'
            elif rec.issue_type == 'structural':
                rec.priority = 'high'
            elif rec.issue_type == 'electrical':
                rec.priority = 'medium'
            else:
                rec.priority = False

    @api.depends('create_date', 'priority', 'resolved_date')
    def _compute_is_overdue(self):
        for rec in self:
            if not rec.create_date:
                rec.is_overdue = False
                continue

            if rec.priority == 'high':
                days = 2
            elif rec.priority == 'medium':
                days = 5
            else:
                days = 10

            deadline = rec.create_date + timedelta(days=days)
            end_time = rec.resolved_date or fields.Datetime.now()
            rec.is_overdue = end_time > deadline

    @api.onchange("salesman_id")
    def _onchange_salesman_id(self):
        if self.salesman_id:
            self.staty = 'in_progress'

    def action_resolve(self):
        for rec in self:
            rec.staty = 'resolved'
            rec.resolved_date = fields.Datetime.now()

    def action_cancel(self):
        for rec in self:
            rec.staty = 'canceled'
