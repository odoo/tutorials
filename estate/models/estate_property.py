from odoo import models, fields


class EstatePropertyModel(models.Model):
    _name = 'estate.property'
    _description = "Estate Property Model"

    name = fields.Char(string="Title", required=True)
    property_type_id = fields.Many2one(
        "estate.property.type", string="Property Type")
    description = fields.Text()
    postcode = fields.Char(string="Postal code")
    date_availability = fields.Date(string="Available From", copy=False,
                                    default=lambda self: fields.Date.add(fields.Date.today(), months=3))
    buyer_id = fields.Many2one(comodel_name="res.users", string="Buyer", copy=False)
    salesperson_id = fields.Many2one(comodel_name="res.partner", string="Salesperson", default=lambda self: self.env.user)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(string="No of Bedrooms", default=2.00)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Number of Facades")
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West'),
        ]
    )
    active = fields.Boolean(default=True)
    status = fields.Selection(
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled'),
        ]
    )
