from dataclasses import field

from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.misc import unique


class MeetingBuilding:
    _name = "meeting.building"
    _description = "Meeting Building"
    _order = "name"
            
    code = fields.Char("code of the building", required=True, copy=False)
    number_of_rooms = fields.Integer("Number Of Rooms", required=True, default=1)
    working_time_start = fields.Float("Working Time Start (UTC)", required=True,
                default=8.0, help="When does work start.")
    working_time_end = fields.Float("Working Time End (UTC)", required=True,
                default=18.0, help="When does work ends.")
    active = fields.Boolean("Active", default=True)
    
    room_ids = fields.One2many('meeting.room', 'building_ids')


    _sql_constrains = [
        ("code_unique", "UNIQUE(code)", "Building code must be unique!"),
        ("check_number_of_rooms", "CHECK(number_of_rooms > 0)", "Number of rooms must be strictly positive!"),
        ("check_working_hours", "CHECK(working_time_start < working_time_end)", "Working time start must be earlier than end time!"),
        ("check_working_hours_range", "CHECK(working_time_start >= 0.0 AND working_time_end <= 24.0)", "Working hours must be between 00:00 and 24:00 UTC!"),
    ]

    @api.depends("room_ids")
    def _compute_number_of_rooms(self):
        for building in self:
            building.number_of_rooms = len(building.room_ids)