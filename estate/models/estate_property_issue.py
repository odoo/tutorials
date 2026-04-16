from datetime import timedelta

from odoo import api, fields, models
from odoo.orm.models import UserError


class Estatepropertyissue(models.Model):
    _name = 'estate.property.issue'
    _description = "Estate Property issues"

    name = fields.Char(required=True)
    property_id = fields.Many2one('estate.property', string='Property Name', required=True)
    reported_by = fields.Many2one('res.partner', string='Reported by')
    assigned_to = fields.Many2one('res.users', string='assigned to')

    issue_type = fields.Selection(
        [
            ('plumbing', "Plumbing"),
            ('electrical', "Electrical"),
            ('structural', "Structural"),
            ('other', "Other")
        ], required=True
    )

    state = fields.Selection(
        [
            ('new', "New"),
            ('in_progress', "In progress"),
            ('resolved', "Resolved"),
            ('cancelled', "Cancelled")
        ], default='new', readonly=True
    )

    priority = fields.Selection(
        [
            ('low', "Low"),
            ('medium', "Medium"),
            ('high', "High"),
        ], store=True, compute="_compute_priority",
    )

    reported_date = fields.Datetime(default=fields.Date.today())
    resolved_date = fields.Datetime(readonly=True)
    description = fields.Text()

    sla_deadline = fields.Datetime(compute="_compute_sla_deadline", store=True, string='Due Deadline')
    is_due = fields.Boolean(compute="_compute_is_due", store=True)

    @api.depends('priority', 'reported_date')
    def _compute_sla_deadline(self):
        for record in self:
            if record.priority == "high":
                record.sla_deadline = record.reported_date + timedelta(days=2)
            elif record.priority == "medium":
                record.sla_deadline = record.reported_date + timedelta(days=5)
            elif record.priority == "low":
                record.sla_deadline = record.reported_date + timedelta(days=10)

    @api.depends('sla_deadline', 'create_date')
    def _compute_is_due(self):
        now = fields.Datetime.today()
        for record in self:
            record.is_due = False
            if record.sla_deadline and now > record.sla_deadline:
                record.is_due = True

    @api.depends('issue_type')
    def _compute_priority(self):
        for rec in self:
            if rec.issue_type == 'structural':
                rec.priority = 'high'
            elif rec.issue_type == 'electrical':
                rec.priority = 'medium'
            else:
                rec.priority = 'low'

    @api.onchange('assigned_to')
    def _onchange_assigned_to(self):
        for record in self:
            if record.assigned_to:
                record.state = 'in_progress'

    def action_resolve(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError('Cancelled issue can not be resolved')
            if record.state == 'resolved':
                raise UserError('Issue is already resolved.')
            record.state = 'resolved'
            record.resolved_date = fields.Datetime.now()

    def action_cancel(self):
        for rec in self:
            if rec.state == 'cancelled':
                raise UserError('Cancelled issue can not be resolved')
            if rec.state == 'resolved':
                raise UserError('Resolved issue cannot be cancelled.')
            rec.state = 'cancelled'
