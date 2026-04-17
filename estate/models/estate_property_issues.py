from datetime import timedelta
from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatepropertyIssues(models.Model):
    _name = 'estate.property.issues'
    _description = 'Property Issues'

    name = fields.Char(required=True, string="Issue")
    property_id = fields.Many2one('estate.property', string="Property")
    reported_by = fields.Many2one('res.partner', string="Reported By")
    assigned_to = fields.Many2one('res.users', string="Assigned To")
    issue_type = fields.Selection(
        selection=[
        ('plumbing', "Plumbing"), ('electrical', "Electrical"),
        ('structural', "Structural"), ('other', "Other")],
        required=True
    )
    issue_state = fields.Selection(
        selection=[
        ('new', "New"), ('in progress', "In Progress"),
        ('resolved', "Resolved"), ('cancelled', "Cancelled")],
        default='new',
        string="Status"
    )
    priority = fields.Selection(
        selection=[
            ('low', "Low"),
            ('medium', "Medium"),
            ('high', "High")],
        readonly=True,
        compute='_compute_priority',
        store=True
    )
    reported_date = fields.Date(string="When reported", default=lambda self: fields.Date.today())
    resolved_date = fields.Date(readonly=True)
    description = fields.Text()
    is_overdue = fields.Boolean(compute='_compute_is_overdue')

    @api.depends('issue_type')
    def _compute_priority(self):
        if self.issue_type == 'other':
            self.priority = 'low'
        if self.issue_type == 'structural':
            self.priority = 'high'
        if self.issue_type in ('plumbing', 'electrical'):
            self.priority = 'medium'

    @api.depends('reported_date', 'priority', 'issue_state')
    def _compute_is_overdue(self):
        for record in self:
            if record.issue_state in ('resolved', 'cancelled'):
                record.is_overdue = False
                continue
            days = {'high': 2, 'medium': 5, 'low': 10}.get(record.priority, 0)
            deadline = record.reported_date + timedelta(days=days)
            record.is_overdue = fields.Date.today() > deadline

    @api.onchange('assigned_to')
    def _onchange_assigned_to(self):
        if self.assigned_to:
            self.issue_state = 'in progress'

    def action_resolve(self):
        for record in self:
            if record.issue_state == 'cancelled':
                raise UserError("Cancelled issues cannot be resolved!")
            record.issue_state = "resolved"
            record.resolved_date = fields.Date.today()
        return True

    def action_cancel(self):
        for record in self:
            record.issue_state = 'cancelled'
        return True
