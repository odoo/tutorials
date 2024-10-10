from odoo import api,fields, models
from datetime import datetime, timedelta

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(default=lambda self: datetime.now() + timedelta(days=90))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True)
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
        ('west', 'West')
    ])

    total_area = fields.Float(compute="_compute_total_area", string="Total Area", store=True)
    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = (record.living_area or 0) + (record.garden_area or 0)

    best_price = fields.Float(compute="_compute_best_price", inverse="_inverse_best_price", string="Best Offer", store=True)
    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price'), default=0.0)
    # def _inverse_best_price(self):
    #     for record in self:
    #         for offer in record.offer_ids:
    #             offer.price = record.best_price

    #         if not record.offer_ids:
    #             self.env['estate.property.offer'].create({
    #                 'property_id': record.id,
    #                 'price': record.best_price,
    #                 'partner_id': self.env.user.partner_id.id,  # Default to current user
    #                 'status': 'pending'  # Example default status
    #             })

    active = fields.Boolean(default=True)
    state = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('canceled', 'Canceled')],
        required=True, default='new')
    property_type_id = fields.Many2one('estate.property.type', string="Property Type")
    buyer_id = fields.Many2one('res.partner', string="Buyer")
    seller_id = fields.Many2one('res.users', string="Salesperson", default=lambda self: self.env.user)
    tag_ids = fields.Many2many('estate.property.tag', string="Tags")
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offers")

    