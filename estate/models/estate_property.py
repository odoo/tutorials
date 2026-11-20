from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "ESTATE property"

    currency_id = fields.Many2one(
        'res.currency',
        default=lambda self: self.env.company.currency_id, required=True)
    name = fields.Char(required=True)
    property_type = fields.Many2one("estate.property.type", string="Partner", required=True)
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=lambda self: fields.Date.today() + relativedelta(months=3))
    expected_price = fields.Monetary(currency_field='currency_id', required=True)
    best_price = fields.Monetary(currency_field='currency_id', compute="_compute_best_price")
    selling_price = fields.Monetary(currency_field='currency_id', readonly=True)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Float()
    facades = fields.Integer()
    garage = fields.Boolean(default=False)
    garden = fields.Boolean(default=False)
    garden_area = fields.Float()
    garden_orientation = fields.Selection([('n', 'N'), ('s', 'S'), ('w', 'W'), ('e', 'E')])
    total_area = fields.Integer(compute="_compute_area")
    active = fields.Boolean(default=True)
    state = fields.Selection([('new', 'New'), ('offer_received', 'Offer received'), ('sold', 'Sold'), ('cancelled', 'Cancelled')], default='new', required=True, string="Status")
    user_id = fields.Many2one('res.users', string='Salesperson', index=True, default=lambda self: self.env.user)
    partner_id = fields.Many2one('res.partner', string='Buyer', index=True)
    tag_ids = fields.Many2many('estate.property.tag', string="Tags")
    offer_ids = fields.One2many('estate.property.offer', "property_id", string="Offers")

    @api.depends("living_area", "garden_area")
    def _compute_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"), default=0.0)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'n'
        else:
            self.garden_area = 0
            self.garden_orientation = False
