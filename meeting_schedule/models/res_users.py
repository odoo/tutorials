from odoo import api, fields, models

class ResUsers(models.Model):
    _inherit = 'res.users'

    reservation_ids = fields.One2many("meeting.reservation", "organizer_id", string="Meeting Reservations")