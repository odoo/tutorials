from odoo import fields, models

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Property estates"

    state = fields.Selection(
        default='New',
        string='Stage',
        selection=[('New', 'New'), ('Offer_Received', 'Offer Received'), ('Offer_Accepted', 'Offer Accepted'), ('Sold', 'Sold'), ('Canceled', 'Canceled')],
    )
    active = fields.Boolean(default=True)


    property_type = fields.Many2one(
        "estate.property.type",
        string="Property Type",
        default=lambda self: self.env['estate.property.type'].search([], limit=1)
    )
    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False, 
        default=fields.Date.add(fields.Date.today(), months=3) # default 3 months from now
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(copy=False, readonly=True)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('North', 'North'), ('East', 'East'), ('South', 'South'), ('West', 'West')],
    )
    buyer_id = fields.Many2one("res.partner", string="Buyer")
    salesperson_id = fields.Many2one("res.users", default=lambda self: self.env.user, string="Salesperson")
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offers_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")