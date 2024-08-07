from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from datetime import date
from odoo.exceptions import UserError, ValidationError


class estate_property(models.Model):
    _name = "estate_property"
    _description = "Estate Property"
    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(default=date.today() + relativedelta(month=3))
    expected_price = fields.Float(readonly= True, required=True)
    selling_price = fields.Float(readonly= True)
    bedrooms = fields.Integer(default=2)
    livingArea = fields.Integer()
    garage = fields.Integer()
    facades = fields.Integer()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    active = fields.Boolean(default=True)
    state = fields.Selection(default='new',
                             selection=[('new', 'New'),
                             ('offer_received', 'Offer Received'),
                             ('offer_accepted', 'Offer Accepted'),
                             ('sold', 'Sold'), ('canceled', 'Canceled')])
    garden_orientation = fields.Selection(selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
    property_type = fields.Many2one("estate_property_type", string="Product Type")
    salesperson_id = fields.Many2one('res.users', string='Selesperson', default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False, ondelete='cascade')
    tag_ids = fields.Many2many("estate_property_tag", string="Tags")
    offer_ids = fields.One2many('estate_property_offer', 'property_id')
    total_area = fields.Float(compute="_compute_total")

    _sql_constraints = [
        ('check_Expected_price', 'CHECK(expected_price > 0)', 'Expected Price must be strictly positive'),
        ('check_selling_price', 'CHECK(selling_price >= 0)', 'Selling Price selling price must be positive'),
        ('unique_name', 'UNIQUE(name)', 'Property type name must be unique')
    ]

    @api.depends()
    def _compute_total(self):
        for record in self:
            record.total_area = record.garden_area + record.livingArea

    best_offer = fields.Float(compute="_best_offer")

    @api.depends('offer_ids')
    def _best_offer(self):
        maximum_price = 0
        for record in self.offer_ids:
            if record.price > maximum_price:
                maximum_price = record.price
        self.best_offer = maximum_price

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = ''
    
    def button_action_sold(self):
        if self.state == "canceled":
            raise UserError("Can't be Sold")
        else:
            self.state = "sold"

    def button_action_cancled(self):
        if self.state == "sold":
            raise UserError("Can't be Cancle, It is already Sold")
        else:
            self.state = "canceled"
    
    @api.constrains('selling_price','expected_price')
    def _price_constrains(self):
        for record in self:
            if record.selling_price > 0:
             if record.selling_price < 0.9*record.expected_price:
                raise ValidationError("Selling price cannot be lower than 90% of the expected price")
             else:
                pass
