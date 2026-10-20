from odoo import fields, models


class Property(models.Model):
    _name = "estate.property"
    _description = "Estate property"

    name = fields.Char(required=True)
    active = fields.Boolean('Active', default=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False,
        default=lambda self: fields.Date.today().replace(month=(fields.Date.today().month + 3) % 12))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Orientation',
        selection=[('south', 'South'), ('north', 'North'), ('east', 'East'), ('west', 'West')]
    )
    state = fields.Selection(
        selection=[('new_property', "New"), ('offer_received', 'Offer received'),
            ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')],
        default='new_property'
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    salesperson_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    tags_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id")
