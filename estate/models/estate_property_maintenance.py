from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class EstatePropertyMaintenance(models.Model):
    _name = "estate.property.maintenance"
    _description = "Property maintenance"

    property_id = fields.Many2one(
        'estate.property',
        string="Property",
        required=True
    )
    issue_type = fields.Selection(
        [
            ('waterleakage', 'Water leakage'),
            ('electrical', 'Electrical'),
            ('plumber', 'Plumbing'),
            ('structure', 'Structural')
        ]
    )
    description = fields.Text()
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
    state = fields.Selection(
        [
            ('new', 'New'),
            ('assign', 'Assign'),
            ('wip', "WIP"),
            ('complete', 'Complete'),
        ],
        default='new'
    )
    date = fields.Date(default=lambda self: fields.Date.today())
    estimated_cost = fields.Integer(compute="_compute_estimated_cost")
    actual_cost = fields.Integer()
    technician = fields.Many2one(
        'res.users',
        string="Assign To",
    )
    total_actual_cost = fields.Integer(
        compute="_compute_total_actual_cost",
    )

    @api.depends("issue_type")
    def _compute_estimated_cost(self):
        for record in self:
            if record.issue_type == 'waterleakage':
                record.estimated_cost = 10000
            elif record.issue_type == 'electrical':
                record.estimated_cost = 20000
            elif record.issue_type == 'structure':
                record.estimated_cost = 50000
            elif record.issue_type == 'plumber':
                record.estimated_cost = 30000
            else:
                record.estimated_cost = 0

    @api.depends("issue_type")
    def _compute_priority(self):
        for record in self:
            if record.issue_type == 'structure':
                record.priority = 'high'
            elif record.issue_type == 'electrical':
                record.priority = 'medium'
            else:
                record.priority = 'low'

    @api.constrains('state', 'actual_cost')
    def _check_actual_cost(self):
        for record in self:
            if record.state == 'complete' and (not record.actual_cost or record.actual_cost <= 0):
                raise ValidationError(_(
                    "Actual Cost must be fill before marking the maintenance as Done."
                ))

    @api.depends('property_id', 'actual_cost')
    def _compute_total_actual_cost(self):
        for record in self:
            if record.property_id:
                maintenance = self.search([
                    ('property_id', '=', record.property_id.id)
                ])
                record.total_actual_cost = sum(
                    maintenance.mapped('actual_cost'))
            else:
                record.total_actual_cost = 0

    def action_create_issue(self):
        for records in self:
            records.state = 'assign'
            records.technician = self.env.user
        return True

    def action_inprogress_issue(self):
        for records in self:
            records.state = 'wip'
        return True

    def action_done_issue(self):
        for records in self:
            records.state = 'complete'
        return True
