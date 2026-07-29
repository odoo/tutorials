from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class AwesomeEstatePropertyMaintenance(models.Model):
    _name = 'awesome.estate.property.maintenance'
    _description = 'Property Maintenance Request'
    _rec_name = 'name'
    _order = 'id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _mail_post_access = 'read'
    _check_company_auto = True

    # -----------------------------------------------------------------------
    # Fields
    # -----------------------------------------------------------------------
    name = fields.Char(string="Title", required=True, tracking=1)
    description = fields.Text()
    issue_type = fields.Selection(
        string="Issue Type",
        default='other',
        required=True,
        tracking=1,
        selection=[
            ('electricity', "Electricity"),
            ('plumbing', "Plumbing"),
            ('carpentry', "Carpentry"),
            ('painting', "Painting"),
            ('cleaning', "Cleaning"),
            ('pest_control', "Pest Control"),
            ('structural', "Structural"),
            ('other', "Other"),
        ],
    )
    property_id = fields.Many2one(
        'awesome.estate.property', string="Property", required=True, ondelete='cascade',
    )
    requester_id = fields.Many2one(
        'res.partner', string="Requested By",
        required=True, default=lambda self: self.env.user.partner_id.id,
    )
    is_tenant = fields.Boolean(string="Is Tenant", default=False)
    technician_id = fields.Many2one(
        'res.users', string="Technician",
        domain="[('share', '=', False)]",
        index='btree_not_null',
        tracking=1,
    )
    priority = fields.Selection(
        string="Priority",
        default='2',
        required=True,
        tracking=1,
        selection=[
            ('0', "Very Low"),
            ('1', "Low"),
            ('2', "Normal"),
            ('3', "High"),
        ],
    )
    company_id = fields.Many2one(
        'res.company', string="Company",
        required=True, default=lambda self: self.env.company,
    )
    currency_id = fields.Many2one(
        'res.currency', string="Currency",
        default=lambda self: self.env.company.currency_id.id,
        required=True,
    )
    estimate_cost = fields.Monetary(
        string="Estimated Cost", currency_field='currency_id',
        tracking=10,
    )
    actual_cost = fields.Monetary(
        string="Actual Cost", currency_field='currency_id',
        compute='_compute_actual_cost', store=True,
        tracking=20,
    )
    cost_line_ids = fields.One2many(
        'awesome.estate.property.maintenance.cost',
        'maintenance_id', string="Cost Lines",
    )
    subtask_ids = fields.One2many(
        'awesome.estate.property.maintenance.subtask',
        'maintenance_id', string="Subtasks",
    )
    request_date = fields.Date(
        string="Request Date",
        default=fields.Date.context_today, required=True,
    )
    schedule_date = fields.Datetime(string="Scheduled Date")
    close_date = fields.Date(string="Completion Date", readonly=True)
    internal_notes = fields.Html(string="Internal Notes")
    progress = fields.Integer(
        string="Progress (%)",
        compute='_compute_progress', store=True,
    )
    state = fields.Selection(
        string="Status",
        default='new', required=True, copy=False,
        tracking=50,
        selection=[
            ('new', "New"),
            ('assigned', "Assigned"),
            ('in_progress', "In Progress"),
            ('done', "Done"),
            ('canceled', "Canceled"),
        ],
    )

    # -----------------------------------------------------------------------
    # SQL Constraints
    # -----------------------------------------------------------------------
    _check_progress = models.Constraint(
        'CHECK(progress >= 0 AND progress <= 100)',
        "Progress must be between 0 and 100%.",
    )

    # -----------------------------------------------------------------------
    # Python Constraints
    # -----------------------------------------------------------------------
    @api.constrains('state', 'technician_id')
    def _check_assigned_requires_technician(self):
        for record in self:
            if record.state == 'assigned' and not record.technician_id:
                raise ValidationError(
                    _("An assigned maintenance request must have a technician."),
                )

    # -----------------------------------------------------------------------
    # Compute Methods
    # -----------------------------------------------------------------------
    @api.depends('subtask_ids.cost', 'cost_line_ids.amount')
    def _compute_actual_cost(self):
        """Actual cost = sum of all subtask costs + general cost lines."""
        for record in self:
            subtask_cost = sum(record.subtask_ids.mapped('cost'))
            line_cost = sum(record.cost_line_ids.mapped('amount'))
            record.actual_cost = subtask_cost + line_cost

    @api.depends('subtask_ids.state')
    def _compute_progress(self):
        """Progress % = (done subtasks / active subtasks) * 100.

        Canceled subtasks are excluded from both numerator and denominator
        so they do not distort the progress bar.
        """
        for record in self:
            active = record.subtask_ids.filtered(
                lambda s: s.state != 'canceled')
            total = len(active)
            if not total:
                record.progress = 0
                continue
            done = len(active.filtered(lambda s: s.state == 'done'))
            record.progress = int((done / total) * 100)

    # -----------------------------------------------------------------------
    # Onchange Methods
    # -----------------------------------------------------------------------
    @api.onchange('issue_type')
    def _onchange_issue_type(self):
        """Auto-fill estimate cost from issue type."""
        ISSUE_TYPE_DEFAULT_COST = {
            'electricity': 1000.0,
            'plumbing': 1500.0,
            'carpentry': 2000.0,
            'painting': 5000.0,
            'cleaning': 2000.0,
            'pest_control': 2500.0,
            'structural': 10000.0,
            'other': 1000.0,
        }
        if self.issue_type:
            self.estimate_cost = ISSUE_TYPE_DEFAULT_COST.get(self.issue_type, 1000.0)

    @api.onchange('technician_id')
    def _onchange_technician(self):
        """Auto-transition new -> assigned when technician is selected."""
        if self.technician_id and self.state == 'new':
            self.state = 'assigned'
        if not self.technician_id and self.state == 'assigned':
            self.state = 'new'

    # -----------------------------------------------------------------------
    # CRUD Methods
    # -----------------------------------------------------------------------
    @api.model_create_multi
    def create(self, vals_list):
        """Prevent creating maintenance requests on sold or canceled properties.

        Skip validation during module data loading (demo/seed data) to allow
        XML data files to seed records correctly.  This follows the established
        pattern from enterprise/account_3way_match.
        """
        if not self.env.context.get('module'):
            for vals in vals_list:
                if vals.get('property_id'):
                    property = self.env['awesome.estate.property'].browse(vals['property_id'])
                    if property.state in ('sold', 'canceled'):
                        raise UserError(_(
                            "Cannot create maintenance requests on %s properties.",
                            property.state,
                        ))
        return super().create(vals_list)

    @api.ondelete(at_uninstall=False)
    def _unlink_if_not_final(self):
        """Prevent deletion of requests that are in progress or completed."""
        for record in self:
            if record.state not in ('new', 'canceled'):
                raise UserError(
                    _("Cannot delete a maintenance request in '%s' state. "
                      "Cancel it first.", record.state))

    # -----------------------------------------------------------------------
    # Action Methods
    # -----------------------------------------------------------------------
    def action_assign(self):
        """Assign the technician and move to 'assigned' state."""
        self.ensure_one()
        if self.state != 'new':
            raise UserError(_("Only new requests can be assigned."))
        if not self.technician_id:
            raise UserError(_("Select a technician before assigning."))
        self.state = 'assigned'
        return True

    def action_start(self):
        """Start work on the request."""
        self.ensure_one()
        if self.state != 'assigned':
            raise UserError(_("Assign the request before starting work."))
        self.state = 'in_progress'
        return True

    def action_done(self):
        """Complete the request. Requires estimate_cost and all subtasks done."""
        self.ensure_one()
        if self.state not in ('assigned', 'in_progress'):
            raise UserError(
                _("Only assigned or in-progress requests can be completed."))
        if not self.estimate_cost:
            raise UserError(
                _("Set an estimated cost before completing this request."))
        if self.subtask_ids:
            pending = self.subtask_ids.filtered(
                lambda s: s.state not in ('done', 'canceled'))
            if pending:
                raise UserError(
                    _("Complete all subtasks before marking this request as done. "
                      "Pending: %s", ', '.join(pending.mapped('name'))))
        self.write({
            'state': 'done',
            'close_date': fields.Date.today(),
            'progress': 100,
        })
        return True

    def action_cancel(self):
        """Cancel the request. Needs a reason in internal_notes if work started."""
        self.ensure_one()
        if self.state == 'done':
            if not self.internal_notes:
                raise UserError(
                    _("Completed requests require a cancellation reason in Internal Notes."))
            self.write({
                'state': 'canceled',
                'close_date': fields.Date.today(),
                'progress': 0,
            })
            return True
        if self.state in ('assigned', 'in_progress'):
            if not self.internal_notes:
                raise UserError(
                    _("Provide a cancellation reason in Internal Notes."))
        self.write({
            'state': 'canceled',
            'close_date': fields.Date.today(),
            'progress': 0,
        })
        return True

    def action_reset(self):
        """Reopen a done or canceled request back to 'new'."""
        self.ensure_one()
        if self.state not in ('done', 'canceled'):
            raise UserError(
                _("Only done or canceled requests can be reset."))
        self.write({
            'state': 'new',
            'progress': 0,
            'close_date': False,
        })
        return True

    # -----------------------------------------------------------------------
    # Cron Methods
    # -----------------------------------------------------------------------
    @api.model
    def _cron_escalate_overdue_maintenance(self):
        """Daily cron: warn on maintenance requests past their scheduled date."""
        overdue = self.search([
            ('state', 'in', ('assigned', 'in_progress')),
            ('schedule_date', '<', fields.Datetime.now()),
        ])
        for record in overdue:
            record.message_post(
                body=_(
                    "This maintenance request is overdue (scheduled for %s). "
                    "Please take appropriate action.",
                    record.schedule_date,
                )
            )
        return True
