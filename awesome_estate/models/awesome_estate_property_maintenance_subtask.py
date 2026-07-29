from odoo import _, fields, models
from odoo.exceptions import UserError


class AwesomeEstatePropertyMaintenanceSubtask(models.Model):
    _name = 'awesome.estate.property.maintenance.subtask'
    _description = 'Maintenance Subtask'
    _rec_name = 'name'
    _order = 'sequence, id'

    # -----------------------------------------------------------------------
    # Fields
    # -----------------------------------------------------------------------
    maintenance_id = fields.Many2one(
        'awesome.estate.property.maintenance',
        string="Maintenance Request",
        required=True,
        ondelete='cascade',
        index=True,
    )
    name = fields.Char(string="Task", required=True)
    technician_id = fields.Many2one(
        'res.users',
        string="Assigned To",
        default=lambda self: self.env.user,
        domain="[('share', '=', False)]",
    )
    state = fields.Selection(
        string="Status",
        default='pending',
        required=True,
        selection=[
            ('pending', "Pending"),
            ('in_progress', "In Progress"),
            ('done', "Done"),
            ('canceled', "Canceled"),
        ],
    )
    sequence = fields.Integer(string="Order", default=10)
    planned_hours = fields.Float(string="Planned Hours")
    effective_hours = fields.Float(string="Effective Hours")
    cost = fields.Monetary(string="Cost", currency_field='currency_id')
    currency_id = fields.Many2one(
        'res.currency',
        related='maintenance_id.currency_id',
        store=True,
    )
    description = fields.Text(string="Work Notes")

    # -----------------------------------------------------------------------
    # Action Methods
    # -----------------------------------------------------------------------
    def action_start(self):
        self.ensure_one()
        if self.state != 'pending':
            raise UserError(_("Only pending subtasks can be started."))
        self.state = 'in_progress'

    def action_done(self):
        self.ensure_one()
        if self.state not in ('in_progress', 'pending'):
            raise UserError(
                _("Only in-progress or pending subtasks can be marked done."))
        self.write({
            'state': 'done',
            'effective_hours': self.effective_hours or self.planned_hours,
        })

    def action_cancel(self):
        self.ensure_one()
        if self.state == 'done':
            raise UserError(_("Completed subtasks cannot be canceled."))
        self.state = 'canceled'
