from dateutil.relativedelta import relativedelta
from odoo import api, fields, models


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property'

    name = fields.Char(string="Title", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Available From", copy=False, default=lambda self: fields.Date.today() + relativedelta(months=3))
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area (spm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area (spm)")
    total_area = fields.Float(string="Total Area (sqm)", compute="_computed_total_area", store=True)
    garden_orientation = fields.Selection([
        ('north', "North"),
        ('east', "East"),
        ('west', "West"),
        ('south', "South")
    ])
    active = fields.Boolean(string="Active", default=True)
    state = fields.Selection([
        ('new', "New"),
        ('offer_received', "Offer Received"),
        ('offer_accepted', "Offer Accepted"),
        ('sold', "Sold"),
        ('cancelled', "Cancelled")
    ], string="State", copy=False, default='new')
    property_type_id = fields.Many2one('estate.property.type', string="Property Type", ondelete="cascade")
    sales_person_id = fields.Many2one('res.users', string='Salesman', ondelete='cascade')
    buyer_id = fields.Many2one('res.partner', string='Buyer', ondelete='cascade')
    property_tag_ids = fields.Many2many('estate.property.tag')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offers")

    @api.depends("living_area", "garden_area")
    def _computed_total_area(self):
        for rec in self:
            rec.total_area = rec.living_area + rec.garden_area
