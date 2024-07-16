from odoo import fields, models
from dateutil.relativedelta import relativedelta


class EstateModel(models.Model):
    _name = 'estate.property'
    _description = "Estate"

    name = fields.Char()
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=(fields.Date.today() + relativedelta(months=3)))
    expected_price = fields.Float()
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string="Orientation",
        selection=[('north', "North"), ('south', "South"), ('east', "East"), ('west', "West")],
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string="Status",
        selection=[('new', "New"), ('offer_received', "Offer Received"), ('offer_accepted', "Offer Accepted"),
                   ('sold', "Sold"), ('canceled', "Canceled")],
        required=True,
        copy=False,
        default='new',
    )
    property_type_id = fields.Many2one('estate.property.type', string="Property Type")
    buyer_id = fields.Many2one('res.partner', string="Buyer")
    salesperson_id = fields.Many2one('res.users', string="Sales Person")
    tag_ids = fields.Many2many('estate.property.tag', string="Tags")
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offers")
