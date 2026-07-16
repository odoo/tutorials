from odoo import fields, models


class HackathonSession(models.Model):
    _name = 'hackathon.session'
    _description = 'Hackathon Session'

    name = fields.Char(string='Session Name', required=True)
    start_time = fields.Datetime(string='Start Time')
    end_time = fields.Datetime(string='End Time')
    duration = fields.Float(string='Duration (Hours)')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('done', 'Done')
    ], string='Status', default='draft')
