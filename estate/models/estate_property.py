from odoo import fields, models

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "ch3 exercise tutorial"

    name = fields.Char(required=True)
    # active = fields.Boolean(default=False)
    state = fields.Selection(
        string='Property State',
        selection= [('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')]
    )
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(default=lambda _: fields.Date.add(fields.Date.today(), months=3) , copy=False)
    expected_price = fields.Float()
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default="2")
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string = 'Garden Orientation',
        selection = [('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')]
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer = fields.Many2one("res.partner", string="Buyer", copy=False)
    sales_person = fields.Many2one("res.users", string="Sales Person", default=lambda self: self.env.user)
    property_tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id")
