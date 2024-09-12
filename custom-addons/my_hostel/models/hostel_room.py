from odoo import fields, models, api


class HostelRoom(models.Model):
    _name = 'hostel.room'
    _description = 'Information about hostel'

    room_name = fields.Char('Room Name', help='Enter the name of the room')
    room_number = fields.Char('Room No', help='Enter the room number')
    floor_number = fields.Integer('Floor Number', help='Enter the floor number of the room')
    rent_amount = fields.Monetary('Rent Amount', currency_field='currency_id', help='Enter the rent amount per month')
    currency_id = fields.Many2one('res.currency', string='Currency')
