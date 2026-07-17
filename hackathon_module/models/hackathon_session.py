from odoo import api, fields, models


class HackathonSession(models.Model):
    _name = 'hackathon.session'
    _description = 'Hackathon Session'

    name = fields.Char(string='Hackathon Name', required=True)
    start_time = fields.Datetime(string='Start Time')
    end_time = fields.Datetime(string='End Time')
    duration = fields.Char(string='Duration', compute='_compute_duration', store=True)

    @api.depends('start_time', 'end_time')
    def _compute_duration(self):
        for record in self:
            if record.start_time and record.end_time:
                delta = record.end_time - record.start_time
                total_seconds = int(delta.total_seconds())
                hours, remainder = divmod(total_seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                record.duration = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            else:
                record.duration = "00:00:00"
    venue = fields.Char(string='Venue')
    team_ids = fields.One2many('hackathon.team', 'session_id', string='Teams')
    team_count = fields.Integer(compute='_compute_team_count', string='Team Count')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('done', 'Done')
    ], string='Status', default='draft')

    def _compute_team_count(self):
        for record in self:
            record.team_count = len(record.team_ids)

    def action_start(self):
        for record in self:
            record.state = 'in_progress'
            
    def action_done(self):
        for record in self:
            record.state = 'done'

    def action_view_teams(self):
        self.ensure_one()
        action = self.env['ir.actions.act_window']._for_xml_id('hackathon_module.action_hackathon_team')
        action['domain'] = [('session_id', '=', self.id)]
        action['context'] = {'default_session_id': self.id}
        return action
