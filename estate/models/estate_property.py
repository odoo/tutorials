from dateutil.relativedelta import relativedelta

from odoo import fields, models


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
    selling_price = fields.Monetary(currency_field='currency_id', readonly=True)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Float()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Float()
    garden_orientation = fields.Selection([('n', 'N'), ('s', 'S'), ('w', 'W'), ('e', 'E')])
    active = fields.Boolean(default=True)
    status = fields.Selection([('_new', 'New'), ('offer_received', 'Offer received'), ('sold', 'Sold'), ('cancelled', 'Cancelled')], default='_new', required=True)
    user_id = fields.Many2one('res.users', string='Salesperson', index=True, default=lambda self: self.env.user)
    partner_id = fields.Many2one('res.partner', string='Buyer', index=True)
    tag_ids = fields.Many2many('estate.property.tag', string="Tags")
    offer_ids = fields.One2many('estate.property.offer', "property_id", string="Offers")
