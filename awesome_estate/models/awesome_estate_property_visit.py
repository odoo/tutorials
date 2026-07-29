from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class AwesomeEstatePropertyVisit(models.Model):
    _name = 'awesome.estate.property.visit'
    _description = 'Property Visit'
    _rec_name = 'display_name'
    _order = 'visit_time_start desc'

    # -----------------------------------------------------------------------
    # Fields
    # -----------------------------------------------------------------------
    property_id = fields.Many2one(
        'awesome.estate.property', string="Property", required=True, ondelete='cascade'
    )
    customer_id = fields.Many2one(
        'res.partner', string="Customer", required=True,
        help="The prospective buyer / visitor."
    )
    visitor_id = fields.Many2one(
        related='customer_id', store=False,
        string="Visitor",
        help="Alias for customer_id for backward compatibility."
    )
    agent_id = fields.Many2one(
        'res.users', string="Agent",
        default=lambda self: self.env.user,
        required=True,
        index=True,
        domain="[('share', '=', False)]",
        help="The salesperson conducting the visit."
    )
    visit_time_start = fields.Datetime(
        string="Visit Start", required=True, default=fields.Datetime.now,
    )
    visit_time_end = fields.Datetime(
        string="Visit End",
        help="Leave empty for a time-slot visit. Required for overlap checks.",
    )
    duration = fields.Float(
        string="Duration (hours)",
        compute='_compute_duration', store=True, readonly=False,
        help="Auto computed when start and end are set. May be overridden.",
    )
    state = fields.Selection(
        string="Status",
        default='scheduled',
        required=True,
        selection=[
            ("scheduled", "Scheduled"),
            ("completed", "Completed"),
            ("cancelled", "Cancelled"),
        ],
    )
    rating = fields.Selection(
        string="Rating",
        selection=[
            ("1", "1 - Poor"),
            ("2", "2 - Fair"),
            ("3", "3 - Good"),
            ("4", "4 - Very Good"),
            ("5", "5 - Excellent"),
        ],
        help="Rating of the visit (can be set after completion).",
    )
    notes = fields.Text(string="Notes")

    is_today = fields.Boolean(
        string="Is Today",
        compute='_compute_is_today',
        search='_search_is_today',
    )
    is_mine = fields.Boolean(
        string="Is Mine",
        compute='_compute_is_mine',
        search='_search_is_mine',
    )

    # -----------------------------------------------------------------------
    # Compute Methods
    # -----------------------------------------------------------------------
    @api.depends('visit_time_start', 'visit_time_end')
    def _compute_duration(self):
        for visit in self:
            if visit.visit_time_start and visit.visit_time_end:
                delta = visit.visit_time_end - visit.visit_time_start
                visit.duration = delta.total_seconds() / 3600.0
            else:
                visit.duration = 0.0

    @api.depends('visit_time_start')
    def _compute_is_today(self):
        now = fields.Datetime.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start.replace(hour=23, minute=59, second=59)
        for visit in self:
            if visit.visit_time_start:
                visit.is_today = today_start <= visit.visit_time_start <= today_end
            else:
                visit.is_today = False

    def _search_is_today(self, operator, value):
        if operator not in ('=', '!='):
            raise NotImplementedError(_("Only = and != are supported for is_today."))
        now = fields.Datetime.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start.replace(hour=23, minute=59, second=59)
        if (operator == '=' and value) or (operator == '!=' and not value):
            return [('visit_time_start', '>=', today_start), ('visit_time_start', '<=', today_end)]
        else:
            return [
                '|',
                ('visit_time_start', '<', today_start),
                ('visit_time_start', '>', today_end),
            ]

    @api.depends('agent_id')
    def _compute_is_mine(self):
        for visit in self:
            visit.is_mine = visit.agent_id == self.env.user

    def _search_is_mine(self, operator, value):
        if operator not in ('=', '!='):
            raise NotImplementedError(_("Only = and != are supported for is_mine."))
        if (operator == '=' and value) or (operator == '!=' and not value):
            return [('agent_id', '=', self.env.user.id)]
        return [('agent_id', '!=', self.env.user.id)]

    # -----------------------------------------------------------------------
    # Constraints
    # -----------------------------------------------------------------------
    @api.constrains('visit_time_start', 'visit_time_end', 'property_id')
    def _check_visit_overlap(self):
        """No two scheduled visits for the same property can overlap."""
        for visit in self:
            if visit.state != 'scheduled':
                continue
            start = visit.visit_time_start
            end = visit.visit_time_end
            if not start:
                continue
            if end and start >= end:
                raise ValidationError(
                    _("Visit end time must be after start time.")
                )
            domain = [
                ('property_id', '=', visit.property_id.id),
                ('id', '!=', visit.id),
                ('state', '=', 'scheduled'),
            ]
            if end:
                domain += [('visit_time_start', '<', end), ('visit_time_end', '>', start)]
            else:
                domain += [('visit_time_start', '=', start)]
            overlapping = self.search(domain)
            if overlapping:
                raise ValidationError(
                    _("This property already has a visit scheduled during this time slot.")
                )

    @api.constrains('visit_time_start', 'visit_time_end', 'agent_id')
    def _check_agent_availability(self):
        """No time clash — an agent cannot be at two visits at the same time."""
        for visit in self:
            if visit.state != 'scheduled':
                continue
            start = visit.visit_time_start
            end = visit.visit_time_end
            if not start or not visit.agent_id:
                continue
            if end and start >= end:
                continue
            domain = [
                ('agent_id', '=', visit.agent_id.id),
                ('id', '!=', visit.id),
                ('state', '=', 'scheduled'),
            ]
            if end:
                domain += [('visit_time_start', '<', end), ('visit_time_end', '>', start)]
            else:
                domain += [('visit_time_start', '=', start)]
            clashing = self.search(domain)
            if clashing:
                clashing_name = clashing[0].display_name
                raise ValidationError(
                    _(
                        "Agent %(agent)s is already scheduled for visit '%(visit)s' "
                        "during this time slot.",
                        agent=visit.agent_id.display_name,
                        visit=clashing_name,
                    )
                )

    @api.constrains('visit_time_start')
    def _check_visit_not_in_past(self):
        for visit in self:
            if (
                visit.visit_time_start
                and visit.visit_time_start < fields.Datetime.now()
                and self.env.context.get('allow_past_visit') != True
            ):
                raise ValidationError(_("Visit cannot be scheduled in the past."))

    # -----------------------------------------------------------------------
    # Auto-assign agent from property salesperson (on create, if not set)
    # -----------------------------------------------------------------------
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('agent_id'):
                property_id = vals.get('property_id')
                if property_id:
                    prop = self.env['awesome.estate.property'].browse(property_id)
                    if prop.salesperson_id:
                        vals['agent_id'] = prop.salesperson_id.id
        return super().create(vals_list)

    @api.onchange('property_id')
    def _onchange_property_id(self):
        if self.property_id and self.property_id.salesperson_id:
            self.agent_id = self.property_id.salesperson_id
