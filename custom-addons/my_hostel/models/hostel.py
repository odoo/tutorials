from odoo import fields, models, api


class Hostel(models.Model):
    _name = 'hostel.hostel'  # iternal global unique identifier
    _description = 'Information about hostel'  # descr. of the model.If not provided, will show warning in the log.
    _order = 'id desc, name'  # order by id in descending order
    _rec_name = 'hostel_code'  # name of the field that will be used as a display name

    name = fields.Char(string='Hostel Name', required=True)  # store strings
    hostel_code = fields.Char(string='Code', required=True)

    street = fields.Char('Street')
    street_2 = fields.Char('Street2')

    zip = fields.Char('Zip', change_default=True)
    city = fields.Char('City')
    state_id = fields.Many2one('res.country.state', string='State')
    country_id = fields.Many2one('res.country', string='Country')

    phone = fields.Char('Phone')
    mobile = fields.Char('Mobile', required=True)

    email = fields.Char('Email')

    hostel_floors = fields.Integer('Total Floors', default=6)  # store integers
    image = fields.Binary('Image')  # store images/ files
    active = fields.Boolean('Active', default=True,
                            help='If unchecked, it will allow you to hide the hostel without removing it.')  # store boolean values

    type = fields.Selection([  # store selection values
        ('male', 'Boys'),
        ('female', 'Girls'),
        ('common', 'Common')],
        string='Type',
        help='Type of Hostel',
        required=True,
        default='common')

    other_info = fields.Text('Other Information', help='Enter more information about the hostel')  # store text

    description = fields.Html('Description', help='Enter a description for the hostel')  # store rich text in html
    hostel_rating = fields.Float('Hostel Average Rating', digits='Rating Value',
                                 help='Enter the rating of the hostel')  # store float values

    @api.depends('hostel_code')
    def _compute_display_name(self):
        """This function creates a name for the record based on the hostel name and hostel code."""
        for record in self:
            name = record.name
            if record.hostel_code:
                name = f'{name} ({record.hostel_code})'

            record.display_name = name
