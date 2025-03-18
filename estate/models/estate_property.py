from odoo import fields, models

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "estate property descripction"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default = fields.Date.add(fields.Date.today(), months=+3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facedes = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')]
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string='State',
        selection = [('new', 'New'), ('offer received', 'Offer Received'), ('offer accepted', 'Offer Accpeted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')],
        default = 'new'
    )
    property_type_id = fields.Many2one("estate.property.type", string="Type")
    sale_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.uid)
    buyer_id = fields.Many2one('res.partner', string='Buyer')
    tag_ids = fields.Many2many('estate.property.tag')
    offer_ids = fields.One2many('estate.property.offer', 'property_id')