from odoo import fields, models
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property discription"

    name = fields.Char('name', required=True)
    description = fields.Text('description')
    postcode = fields.Char('postcode')
    availability_date = fields.Date(
        'availabilty date', copy=False, default=fields.Date.today() + relativedelta(months=3))
    expected_price = fields.Float('expected price', required=True)
    selling_price = fields.Float('selling price', readonly=True, copy=False)
    bedrooms = fields.Integer('bedrooms', default=2)
    living_area = fields.Integer('living area')
    facades = fields.Integer('facades')
    garage = fields.Boolean('garage')
    garden_area = fields.Integer('garden area')
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('North', 'North'), ('South', 'South'),
                   ('East', 'East'), ('West', 'West')]
    )
    active = fields.Boolean('active', default=True)
    state = fields.Selection(
        string='State',
        selection=[('new', 'New'), ('offer_received', 'Offer Received'),
                   ('offer_accepted', 'Offer Acccepted'), ('sold', 'Sold'),
                   ('cancelled', 'Cancelled')],
        default="new"
    )
    property_type_id = fields.Many2one(
        "estate.property.type", string="property type")
    user_id = fields.Many2one(
        "res.users", string="Salesperson", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many(
        "estate.property.offer", "property_id", string="Offers")
