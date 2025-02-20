from odoo import fields, models


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'model for the properties in our app'

    name = fields.Char(required = True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy = False,
        default = fields.Date.add(fields.Date.today(), months = 3)
    )
    expected_price = fields.Float(required = True)
    selling_price = fields.Float(readonly = True, copy = False)
    bedrooms = fields.Integer(default = 2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string = "Garden Orientation",
        selection = [
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West'),
        ],
        help = 'garden orientation is used to choose the orientation of the garden attached to the property'
    )
    active = fields.Boolean(default = True)
    state = fields.Selection(
        string = "State",
        selection = [
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled'),
        ],
        default = 'new',
        required = True,
        copy = False,
    )
    property_type_id = fields.Many2one("estate.property.type", string = "Property Type")
    buyer_id = fields.Many2one("res.partner", string = "Buyer", copy = False)
    salesperson_id = fields.Many2one("res.users", string = "Salesperson", default = lambda self: self.env.user)
    property_tag_ids = fields.Many2many("estate.property.tag", string = "Property Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string = "Offers")
