from datetime import timedelta

from odoo import models, fields, api

from odoo.exceptions import UserError


class EstatePropertyIssue(models.Model):
    _name = 'estate.property.issue'
    _description = 'Issues related to estate property'

    name = fields.Char(string="Issue Name", required=True)
    description = fields.Text()
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    reported_by_id = fields.Many2one("res.partner", string="Reported By", copy=False, default=lambda self: self.env.user)
    assigned_to_id = fields.Many2one("res.users", string="Assigned To")
    issue_type = fields.Selection([
            ('plumbing', "Plumbing Issue"),
            ('electrical', "Electrical Issue"),
            ('structural', "Structural Issue"),
            ('other', "Other Issue")
            ], string="Issue Type", required=True)
    state = fields.Selection([
        ('new', "New"),
        ('in_progress', "In Progress"),
        ('resolved', "Resolved"),
        ('overdue', "Overdue"),
        ('cancelled', "Cancelled")
        ], default='new')
    priority = fields.Selection([
        ('low', "Low"),
        ('medium', "Medium"),
        ('high', "High")
        ])
    reported_date = fields.Date(string="Reported Date", readonly=True, default=lambda self: fields.Date.today())
    # reported_date = fields.Date(string="Reported Date")
    resolved_date = fields.Date(string="Resolved Date", readonly=True)
    assigned_date = fields.Date(string="Assigned Date")
    overdue = fields.Boolean(string="Issue Overdue", compute="_compute_overdue")

    @api.onchange("issue_type")
    def _onchange_priority(self):
        for record in self:
            if record.issue_type == 'structural':
                record.priority = 'high'
            elif record.issue_type == 'electrical':
                record.priority = 'medium'
            else:
                record.priority = 'low'

    # @api.onchange("assigned_to_id")
    # def _onchange_assign(self):
    #     for record in self:
    #         if record.assigned_to_id :
    #             print(record.assigned_to_id)
    #             record.state = 'in_progress'

    @api.depends("priority", "state", "assigned_date")
    def _compute_overdue(self):
        for record in self:
            record.overdue = False
            resolve_date = record.resolved_date if record.resolved_date else fields.Date.today()
            start_date = record.assigned_date
            if record.priority == 'high':
                if record.state == 'in_progress' or record.state == 'overdue':
                    if resolve_date - start_date > timedelta(days=2):
                        record.overdue = True
                        record.state = 'overdue'
            elif record.priority == 'medium':
                if record.state == 'in_progress' or record.state == 'overdue':
                    if resolve_date - start_date > timedelta(days=5):
                        record.overdue = True
                        record.state = 'overdue'
            elif record.priority == 'low':
                if record.state == 'in_progress' or record.state == 'overdue':
                    if resolve_date - start_date > timedelta(days=10):
                        record.overdue = True
                        record.state = 'overdue'

    # @api.depends("priority", "state", "create_date")
    # def _compute_overdue(self):
    #     for record in self:
    #         record.overdue = False
    #         resolve_date = record.resolved_date if record.resolved_date else fields.Date.today()
    #         start_date = record.create_date.date()
    #         if record.priority == 'high':
    #             if record.state == 'in_progress' or record.state == 'overdue':
    #                 if resolve_date - start_date > timedelta(days=2):
    #                     record.overdue = True
    #                     record.state = 'overdue'
    #         elif record.priority == 'medium':
    #             if record.state == 'in_progress' or record.state == 'overdue':
    #                 if resolve_date - start_date > timedelta(days=5):
    #                     record.overdue = True
    #                     record.state = 'overdue'
    #         elif record.priority == 'low':
    #             if record.state == 'in_progress' or record.state == 'overdue':
    #                 if resolve_date - start_date > timedelta(days=10):
    #                     record.overdue = True
    #                     record.state = 'overdue'

    def action_resolved(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError("Cancelled property issue cannot be resolved.")
            if record.state != 'in_progress' and record.state != 'overdue':
                raise UserError("Property cannot be resolved until the work has starte.")
            record.state = 'resolved'
            record.resolved_date = fields.Date.today()
        return True

    def action_cancelled(self):
        for record in self:
            if record.state == 'resolved':
                raise UserError("Resolved property issues cannot be cancelled.")
            record.state = 'cancelled'
        return True

    def action_accept(self):
        for record in self:
            record.state = 'in_progress'
            record.assigned_to_id = record.property_id.salesperson_id
            record.assigned_date = fields.Date.today()
        return True
