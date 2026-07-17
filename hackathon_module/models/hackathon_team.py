from odoo import fields, models


class HackathonTeam(models.Model):
    _name = 'hackathon.team'
    _description = 'Hackathon Team'

    name = fields.Char(string='Team Name', required=True)
    session_id = fields.Many2one('hackathon.session', string='Hackathon')
    participant_ids = fields.One2many('hackathon.participant', 'team_id', string='Members')
