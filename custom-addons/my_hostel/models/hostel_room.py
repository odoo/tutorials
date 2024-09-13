from odoo import fields, models, api


class HostelRoom(models.Model):
    _name = 'hostel.room'
    _description = 'Information about hostel room'
    _rec_name = 'room_number'

    room_name = fields.Char('Room Name', help='Enter the name of the room', required=True)
    room_number = fields.Char('Room No', help='Enter the room number', required=True)
    floor_number = fields.Integer('Floor Number', help='Enter the floor number of the room')
    rent_amount = fields.Monetary('Rent Amount', currency_field='currency_id', help='Enter the rent amount per month')
    currency_id = fields.Many2one('res.currency', string='Currency')

    hostel_id = fields.Many2one('hostel.hostel', string='Name of Hostel', required=True)  # used for m2m relation

    student_ids = fields.One2many('hostel.student', 'room_id', string='Students',
                                  help='Select the students for the room')
    hostel_amenities_ids = fields.Many2many('hostel.amenities', 'hostel_room_amenities_rel', 'room_id', 'amenity_id',
                                            string='Amenities', domain=[('active', '=', True)],
                                            help='Select the amenities for the room')

    @api.depends('room_number')
    def _compute_display_name(self):
        """This function creates a name for the record based on the room name and room number."""
        for record in self:
            name = record.room_name
            if record.room_number:
                name = f'{name} ({record.room_number})'

            record.display_name = name
