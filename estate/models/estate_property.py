from odoo import api, fields, models
from datetime import timedelta



class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property Options"
    
    
    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=lambda x: fields.Datetime.add(fields.Datetime.today(), months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[("north", "North"), ("south", "South"), ("east", "East"), ("west", "West")]
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        required=True,
        copy=False,
        default="new",
        selection=[("new", "New"), ("offer_received", "Offer received"), ("offer_accepted", "Offer accepted"), ("sold", "Sold"), ("cancelled", "Cancelled")]
    )

    property_type_id = fields.Many2one(comodel_name="estate.property.type")
    user_id = fields.Many2one(comodel_name='res.users', string='Salesperson', default=lambda self: self.env.user)
    partner_id = fields.Many2one(comodel_name='res.partner', string='Buyer', copy=False)
    property_tag_ids = fields.Many2many(comodel_name='estate.property.tag')
    property_offer_ids = fields.One2many('estate.property.offer','property_id')
    
    
    total_area = fields.Integer(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_price")
    
    
    @api.depends('living_area','garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('property_offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.property_offer_ids.mapped('price'), default=0)

    @api.onchange('garden')
    def _onchange_garden(self):
        self.garden_area = 10 if self.garden else False
        self.garden_orientation = 'n' if self.garden else False

