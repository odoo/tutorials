from odoo import fields, models

class MeetingRoom(models.Model):
    _name = "meeting.room"
    _description = "Meeting Room"
    _order = "building_id, code"

    code = fields.Char("Name", required=True, copy=False)
    active = fields.Boolean("Active", default=True)
    
    building_ids = fields.Many2one('meeting.building', string="Building", required=True, ondelete="cascade")
    reservation_ids = fields.One2many('meeting.reservation', 'room_ids', string="Reservation")

    _sql_constraints = [
        ("building_room_name_uniq", "UNIQUE(building_ids, code)", "Room name must be unique within the same building!"),
    ]