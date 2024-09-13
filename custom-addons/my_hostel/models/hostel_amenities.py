from odoo import fields, models, api


class HostelAmenities(models.Model):
    _name = 'hostel.amenities'
    _description = 'Information about hostel amenities'

    name = fields.Char('Amenity Name', help='Provided Hostel Amenities')
    active = fields.Boolean('Active', default=True,
                            help='If unchecked, it will allow you to hide the amenity without removing it.')
