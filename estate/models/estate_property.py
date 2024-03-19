from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate property"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date("Available from", default=lambda _: fields.Date().add(fields.Date().today(), months=3),
                                    copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer("Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer("Garden Area (sqm)")
    garden_orientation = fields.Selection(string="Garden Orientation",
                                          selection=[("north", "North"), ("south", "South"), ("east", "East"),
                                                     ("west", "West")])
    active = fields.Boolean("Active", default=True)
    state = fields.Selection(string="State", default="new", copy=False, required=True,
                             selection=[("new", "New"), ("offer received", "Offer Received"),
                                        ("offer accepted", "Offer Accepted"), ("sold", "Sold"),
                                        ("canceled", "Canceled")])
    property_type_id = fields.Many2one("estate.property.type", string="Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", index=True, copy=False)
    salesperson_id = fields.Many2one("res.users", string="Salesperson", index=True, default=lambda self: self.env.user)
    property_tag_ids = fields.Many2many("estate.property.tag", string="Tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offer")
