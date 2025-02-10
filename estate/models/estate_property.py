# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Properties"

    name = fields.Char("Title", required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        string="Available From",
        default=lambda self:fields.Date.add(fields.Date.today(), months=3),
        copy=False
        )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(copy=False, readonly=True)
    bedrooms = fields.Integer(index=True, default=2)
    living_area = fields.Integer("Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        selection=[
            ('north','North'),
            ('south','South'),
            ('east','East'),
            ('west','West'),
        ])
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[
            ('new','New'),
            ('offer received','Offer Received'),
            ('offer accepted','Offer Accepted'),
            ('sold','Sold'),
            ('cancelled','Cancelled'),
        ],
        copy=False,
        default='new'
    )
    property_type_id = fields.Many2one('estate.property.type', string="Property Type")
    buyer = fields.Many2one('res.partner', string="Buyer", copy=False)
    salesman = fields.Many2one('res.users', string="Salesman", default=lambda self:self.env.uid)
    tag_ids = fields.Many2many('estate.property.tag')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="offer_id")
    total_area = fields.Integer(compute='_compute_total_area', string="Total Area (sqm)")
    best_offer = fields.Float(compute= '_compute_best_offer', string="Best Offer")

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_offer(self):
        for record in self:
            if record.offer_ids:
                record.best_offer = max(record.offer_ids.mapped('price'))
            else:
                record.best_offer = 0.0
