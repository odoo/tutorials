from datetime import datetime, timedelta
from odoo import api, fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Property's properties"

    name = fields.Char('Property name', required=True, default='Unknown')
    description = fields.Text('Property Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Availability', copy=False, default=datetime.now() + timedelta(days=90))
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Living Area (sqm)')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area')
    garden_orientation = fields.Selection([('North', 'North'), ('East', 'East'), ('South', 'South'), ('West', 'West')], default='North')
    active = fields.Boolean('Active', default=True)
    state = fields.Selection([
        ('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')
    ], default='new', required=True, copy=False)

    total_area = fields.Float("Total Area", compute="_compute_total_area")
    best_price = fields.Float("Best Offer", compute="_compute_best_price")

    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer")
    salesperson_id = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user)
    tags_ids = fields.Many2many("estate.property.tag", string="Tags")
    offers_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    @api.depends("garden_area", "living_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends("offers_ids")
    def _compute_best_price(self):
        for record in self:
            if len(record.offers_ids) == 0:
                record.best_price = 0
                return
            prices = record.offers_ids.mapped("price")
            for price in prices:
                if 0 < price < record.best_price:
                    record.best_price = price

    @api.onchange("garden")
    def _onchange_partner_id(self):
        if self.garden:
            self.garden_orientation = 'North'
            self.garden_area = 10
        else:
            self.garden_orientation = None
            self.garden_area = 0

