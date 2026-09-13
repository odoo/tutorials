from odoo import fields, models

class MeetingRoom(models.Model):
    _name = "meeting.room"
    _description = "Meeting Room"
    _rec_name = "code"
    _order = "building_id, code"

    code = fields.Char("Name", required=True, copy=False)
    active = fields.Boolean("Active", default=True)
    
    building_id = fields.Many2one("meeting.building", string="Building", required=True, ondelete="cascade")
    reservation_ids = fields.One2many("meeting.reservation", "room_id", string="Reservation")

    _sql_constraints = [
        ("building_room_name_uniq", "UNIQUE(building_id, code)", "Room name must be unique within the same building!"),
    ]