from odoo import fields,api,models
from datetime import datetime, timedelta

class EstateProperties(models.Model):
    _name = "estate.property"
    _description = "Estate Model"

    name = fields.Char(required=True)
    id = fields.Integer(required=True)
    create_uid = fields.Integer()
    create_date = fields.Date()
    write_uid = fields.Integer()
    write_date = fields.Date()
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date("Available From" , copy = False , default= datetime.now() + timedelta(days=90))
    last_seen = fields.Datetime("Last Seen", default=fields.Datetime.now)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True , copy = False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ])
    state = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ( 'offer_accepted', 'Offer Accepted'),
        ('sold' , 'Sold'),
        ('canceled' , 'Canceled')],
        required = True, default = "new", copy = False)
    active = fields.Boolean(default=True)
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")  
    buyer_id = fields.Many2one("res.partner",string="Buyer" , copy=False)
    user_id = fields.Many2one("res.users", string="Salesperson" , default=lambda self: self.env.user)
    tag_ids = fields.Many2many('estate.property.tag', string='Tag')
    offer_ids = fields.One2many('estate.property.offer', 'property_id')
    total_area = fields.Float(compute='_compute_total_area')
    best_price = fields.Float(compute="_compute_best_price", store=True)

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
             record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = 0.0
 

        

