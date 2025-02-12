from odoo import api,fields, models 
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError,ValidationError

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Model"
    _order = "id desc"  

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False,
        default= (fields.Date.today() + relativedelta(months=3))
        # default=fields.Date.add(fields.Date.today() , months=3)
    )    
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    is_garage = fields.Boolean()
    is_garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection = [('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
    )
    active = fields.Boolean(default = 'True')
    status = fields.Selection(
        selection = [('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted','Offer Accepted'), ('sold','Sold'), ('cancelled','cancelled')],
        default = 'new'
    )
    property_type_id = fields.Many2one('estate.property.type', string="Property Type")
    buyer_id = fields.Many2one('res.partner', string="Buyer", copy=False)
    seller_id = fields.Many2one('res.users', string="Seller", default=lambda self: self.env.user)
    tag_ids = fields.Many2many('estate.property.tag', string="Tags")
    offer_ids = fields.One2many('estate.property.offer', "property_id", string="Offer")
    total_area = fields.Float(compute="_compute_total")
    best_offer = fields.Float(compute="_compute_offer")

    _sql_constraints = [
        ('expected_price', 'CHECK(expected_price > 0)',
         'The expected price must be strictly positive!'),

        ('selling_price', 'CHECK(selling_price > 0)', 'The selling price must be strictly positive!')
    ]

    @api.depends("living_area","garden_area")
    def _compute_total(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids")
    def _compute_offer(self):
        for record in self:
            if record.offer_ids:
                record.best_offer = max(record.offer_ids.mapped("price"))
            else:
                record.best_offer = 0.0
    
    @api.onchange('is_garden')
    def _onchange_garden(self):
        if self.is_garden == True:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = ''

    @api.constrains('selling_price')
    def _check_offer_price(self):
        for record in self:
            if record.selling_price < (record.expected_price * 0.9) and (record.selling_price > 0):
                raise ValidationError(f"Selling price cannote be lower than 90% of it's expected price!")

    def action_sold(self):
        if self.selling_price<0:
            raise UserError('This property cannot be sold because it selling price is 0 !')
        if self.status == 'cancelled':
            raise UserError('This property cannot be sold it is cancelled')
        self.status='sold'

    def action_cancel(self):
        if self.status == 'sold':
            raise UserError('This property cannot be cancelled it is sold')
        self.status='cancelled'
