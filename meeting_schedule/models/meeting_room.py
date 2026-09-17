from odoo import fields, models, api, _
from odoo.exceptions import ValidationError

class MeetingRoom(models.Model):
    _name = "meeting.room"
    _description = "Meeting Room"
    _rec_name = "code"
    _order = "building_id, code"

    code = fields.Char("Name", required=True, copy=False)
    active = fields.Boolean("Active", default=True)
    seating_capacity = fields.Integer("Seating Capacity", default=8, required=True,
        help="Maximum number of attendees this room can accommodate.")
    
    building_id = fields.Many2one("meeting.building", string="Building",
        required=True, default=lambda self: self._default_building_id(), ondelete="cascade", check_company=True)
    reservation_ids = fields.One2many("meeting.reservation", "room_id", string="Reservation")
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        related="building_id.company_id",
        default=lambda self: self.env.company,
        store=True,
        readonly=True,
        index=True,
    )
    
    _sql_constraints = [
        ("building_room_name_uniq", "UNIQUE(building_id, code)", "Room name must be unique within the same building!"),
        ("check_capacity_positive", "CHECK(seating_capacity > 0)", "seating capacity must be positive!")
    ]

    @api.model
    def _default_building_id(self):
        return self.env['meeting.building'].search([
            '|', ('company_id', '=', False), ('company_id', '=', self.env.company.id)], limit=1)

    @api.constrains("seating_capacity")
    def _check_capacity(self):
        for record in self:
            if record.seating_capacity <= 0:
                raise ValidationError(_("Room capacity must be strictly positive."))