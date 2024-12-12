from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import date, timedelta


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate property table"

    name = fields.Char(string = 'Title', required = True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(string = 'Available From', copy = False, default = date.today() + timedelta(days=90))
    expected_price = fields.Float(required = True)
    selling_price = fields.Float(readonly = True, copy = False)
    bedrooms = fields.Integer(default = 2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection = [
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
            ]
        )
    active = fields.Boolean()
    state = fields.Selection(
        selection = [
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')
            ],
        required = True, copy = False, default = 'new'
        )
    property_type_id = fields.Many2one('estate.property.type', string = 'Property Type', )
    partner_id = fields.Many2one('res.partner', string = 'Buyer')
    user_id = fields.Many2one('res.users', string = 'Salesman', default = lambda self: self.env.user)
    tag_ids = fields.Many2many('estate.property.tags', string = 'Tags')
    offers_id = fields.One2many('estate.property.offer', 'property_id', string = 'Offers')
    total_area = fields.Float(compute = '_compute_total')
    best_price = fields.Float(compute = '_compute_best')

    @api.depends("living_area", "garden_area")
    def _compute_total(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    # @api.onchange("living_area", "garden_area")
    # def _compute_total(record):
    #     record.total_area = record.living_area + record.garden_area

    @api.depends("offers_id")
    def _compute_best(self):
        for record in self:
            record.best_price = max(record.offers_id.mapped('price'),default = 0)

    @api.onchange("garden")
    def _onchange_garden(self):
        self.garden_area = 10 if self.garden else 0
        self.garden_orientation = 'north' if self.garden else None
        # return {
        #     'warning': {'title': "Warning", 'message': "What is this?", 'type': 'notification'},
        #     }
        
    # @api.onchange("garden","garage")
    # def _onchange_garden_garage(self):
    #     if self.garden and self.garage:
    #         self.garden_area = 100
    #         self.garden_orientation = 'north'

    # @api.onchange("property_type_id.name")
    # def _onchange_pt(self):
    #     if self.property_type_id == 'Apartment':
    #         self.garden = 'False'

    # @api.onchange("offers_id")
    # def _onchange_oid(self):
    #     if self.offers_id.price > 100000:
    #         self.state = 'sold'

    # @api.onchange("tag_ids")
    # def _onchange_tags(self):
    #     if self.tag_ids == '2BHK':
    #         self.property_type_id = 'Apartment'

    @api.depends('state')
    def action_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError('Cancelled properties cannot be sold')
            record.state = 'sold'

    @api.depends('state')
    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError('Sold properties cannot be cancelled')
            record.state = 'cancelled'