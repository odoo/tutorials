from odoo import fields, models, api


class HostelStudent(models.Model):
    _name = 'hostel.student'
    _description = 'Information about hostel student'
    name = fields.Char('Student Name', required=True)

    gender = fields.Selection([
        ('male', 'Male'), ('female', 'Female'), ('other', 'Other')
    ], string='Gender', help='Select the gender')
    active = fields.Boolean('Active', default=True,
                            help='If unchecked, it will allow you to hide the student without removing it.')

    room_id = fields.Many2one('hostel.room', string='Room', help='Select the room for the student')
    amenity_id = fields.Many2one('hostel.amenities', string='Amenity',
                                 help='Select the amenity for the student')
