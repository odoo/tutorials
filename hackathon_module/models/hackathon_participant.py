from odoo import fields, models

class HackathonParticipant(models.Model):
    _name = 'hackathon.participant'
    _description = 'Hackathon Participant'

    partner_id = fields.Many2one('res.partner', string='Participant', required=True)
    team_id = fields.Many2one('hackathon.team', string='Team')
    session_id = fields.Many2one('hackathon.session', string='Session')
    status = fields.Selection([
        ('registered', 'Registered'),
        ('active', 'Active'),
        ('finished', 'Finished')
    ], string='Status', default='registered')
