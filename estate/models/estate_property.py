from odoo import fields, models

class EstateModel(models.Model):
    _name = "estate.property"
    _description = "Estate/Property"

    name = fields.Char(required=True, default="New House")
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West")
        ]
    )
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"), 
            ("offer_accepted", "Offer Accepted"), 
            ("sold", "Sold"), 
            ("cancelled", "Cancelled")
        ],
        default="new",
        required=True)
    active = fields.Boolean(default=True)
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson_id = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user)
    property_tags_ids = fields.Many2many("estate.property.tags", string="Property Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="offers")
