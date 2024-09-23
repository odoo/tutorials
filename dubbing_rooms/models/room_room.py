from odoo import fields, models


class RoomRoom(models.Model):
    _inherit = ['room.room']

    availability_ids = fields.One2many('room.availability', 'room_id')
