# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import fields, models, api


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real estate property overview"

    name = fields.Char('Estate name', required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date('Aivailable from', copy=False, default=fields.Date.add(fields.Date.today(), months=3))

    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)

    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()

    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Orientation',
        selection=[('N', 'North'), ('E', 'East'), ('S', 'South'), ('W', 'West')],
        help="Orientation of the garden"
    )

    active = fields.Boolean(default=True)
    state = fields.Selection(
        string='Status',
        selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('canceled', 'Canceled')],
        help='Availability status of the property',
        required=True, copy=False, default='new'
    )

    property_type_id = fields.Many2one("estate.property.type")
    salesman_id = fields.Many2one("res.partner", default=lambda self: self.env.user.partner_id)
    buyer_id = fields.Many2one("res.users")

    tags_ids = fields.Many2many("estate.property.tags", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for estate_property in self:
            estate_property.total_area = estate_property.living_area + estate_property.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for estate_property in self:
            try:
                estate_property.best_price = max(estate_property.offer_ids.mapped('price'))
            except:
                estate_property.best_price = 0

    total_area = fields.Integer(compute=_compute_total_area)
    best_price = fields.Float(compute=_compute_best_price)

    @api.onchange("garden")
    def _onchange_garden(self):
        self.garden_area = 10 if self.garden else 0
        self.garden_orientation = 'N' if self.garden else ''