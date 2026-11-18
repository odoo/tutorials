from odoo import api, fields, models
from odoo.tools import date_utils


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property type"

    name = fields.Char('Name', required=True)


class Property(models.Model):
    _name = "estate.property"
    _description = "Estate property"

    name = fields.Char('Property Name', required=True)
    description = fields.Text('Property Description')
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string='Current Status',
        selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')],
        default='new',
        required=True
    )
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Availability Date', default=lambda self: date_utils.add(fields.Datetime.today(), months=3), copy=False)
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms', help="Number of bedrooms", default=2)
    living_area = fields.Integer('Living Area (m²)')
    facades = fields.Integer('Facades', help="Number of facades")
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area (m²)')
    garden_orientation = fields.Selection(
        string='Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        help="Indicates the orientation of the garden"
    )

    type_id = fields.Many2one("estate.property.type", string="Property Type")
    salesperson_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    tag_ids = fields.Many2many('estate.property.tag', string="Tags")
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offers")

    total_area = fields.Integer('Total Area (m²)', compute="_compute_total_area")
    best_offer = fields.Float('Best Offer', compute="_compute_best_offer")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids")
    def _compute_best_offer(self):
        for record in self:
            best_offer = 0.0 if not record.best_offer else record.best_offer
            for offer in record.offer_ids:
                record.best_offer = max(best_offer, offer.price)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = self.garden_area if self.garden_area else 10
            self.garden_orientation = self.garden_orientation if self.garden_orientation else 'north'
        else:
            self.garden_area = None
            self.garden_orientation = None

    def action_sold(self):
        for record in self:
            record.state = 'sold'

    def action_cancel(self):
        for record in self:
            record.state = 'cancelled'
