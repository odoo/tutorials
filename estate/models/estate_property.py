from odoo import models, fields
from dateutil.relativedelta import relativedelta

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "real state property"

    property_type_id =fields.Many2one(
        "estate.property.type",
        string="Poperty Type"
    )
    buyer_id= fields.Many2one(
        "res.partner", string="buyer", copy=False
    )
    salesperson_id = fields.Many2one(
        "res.users" , string ="sales person" ,default=lambda self: self.env.user
    )

    tag_ids = fields.Many2many(
        "estate.property.tag",
         string="Tags"
    )
    offer_ids = fields.One2many(
        "estate.property.offer",
        'property_id',
        string="Offer"
    )

    


    name = fields.Char(required=True)
    active = fields.Boolean(default=True)

    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False, default=fields.Date.today() + relativedelta(months=3)
    )

    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)

    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()

    garden_area = fields.Integer()

    garden_orientation = fields.Selection(
        [
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ]
    )

    state = fields.Selection(
        [
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ]
    )

    language= fields.selection([
        ('language','Language'),('hindi','Hindi')
    ])