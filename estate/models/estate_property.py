from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "estate property"
    name = fields.Char('Property Name', required=True)
    description = fields.Text('Description', required=False)
    postcode = fields.Char('Postcode', required=False)
    date_availability = fields.Date('Available From', copy=False, default=fields.Datetime.add(fields.Datetime.now(), months=3))
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Living Area (sqm)', default=1)
    facades = fields.Integer('Facades', default=0)
    garage = fields.Boolean('garage', default=False)
    garden = fields.Boolean('garden', default=False)
    garden_area = fields.Integer('garden Area (sqm)', default=0)
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        help="orientation of the garden relative to the porperty")
    active = fields.Boolean('Active')
    state = fields.Selection(
        string='Status',
        selection=[('new', 'New'), 
                   ('offer_received', 'Offer Received'),
                   ('offer_accepted', 'Offer Accepted'),
                   ('sold', 'Sold'),
                   ('canceled', 'Canceled')],
        required=True,
        default='new',
        copy=False)
    property_type_id = fields.Many2one('estate.property.type', string='Type')
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    salesperson_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    property_tag_ids = fields.Many2many('estate.property.tag', string='Tag')
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offer")