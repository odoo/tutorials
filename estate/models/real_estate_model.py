from odoo import fields, models, api
from datetime import timedelta

class EstateModel(models.Model):
    _name = "estate.property"
    _description = "Real estate App"

    name = fields.Char(required = True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy = False, default = lambda self: fields.Date.today() + timedelta(days = 90))
    expected_price = fields.Float(required = True)
    selling_price = fields.Float(readonly = True , copy = False)
    bedrooms = fields.Integer(default = 2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string = 'Garden Orientation',
        selection = [('north','North'),('south','South'), ('east','East'), ('west','West')],
        help = "Select one"
    )
    active = fields.Boolean(default = True)
    state = fields.Selection(
        required = True,
        string = 'Select the status',
        selection = [('new','New'),('offer_received','Offer Received'), ('sold','Sold'), ('cancelled','Cancelled')],
        help = "Select one",
        default = 'new',
        copy = False
    )
    property_type_id = fields.Many2one("estate.property.type", string = "Property Type")
    tag_id = fields.Many2many('estate.property.tags')
    buyer_id = fields.Many2one('res.partner', string = "Buyer")
    seller_id = fields.Many2one('res.users' ,string="Salesperson", default=lambda self: self.env.user)
    offer_ids = fields.One2many('estate.property.offer','property_id', string="Offers")
    total_area = fields.Integer(compute = '_compute_total_area')
    best_offer_price = fields.Float(compute = '_compute_bestprice')

    @api.depends("living_area","garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area


    @api.depends("offer_ids.price")
    def _compute_bestprice(self):
        for record in self:
            record.best_offer_price = max(record.offer_ids.mapped('price'),default=0)


    @api.onchange('garden')
    def _onchange_garden(self):
        if(self.garden == True):
            self.garden_area = 10
            self.garden_orientation = 'north'

        if(self.garden == False):
            self.garden_area = 0
            self.garden_orientation = ''





