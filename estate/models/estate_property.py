from odoo import api, models, fields


class EstatePropertyModel(models.Model):
    _name = 'estate.property'
    _description = "Estate Property Model"

    name = fields.Char(string="Title", required=True)
    property_type_id = fields.Many2one(
        "estate.property.type", string="Property Type")
    property_tag_id = fields.Many2many(
        "estate.property.tag", string="Property Tag")
    description = fields.Text()
    postcode = fields.Char(string="Postal code")
    date_availability = fields.Date(string="Available From", copy=False,
                                    default=lambda self: fields.Date.add(fields.Date.today(), months=3))
    buyer_id = fields.Many2one(comodel_name="res.partner", string="Buyer", copy=False)
    salesperson_id = fields.Many2one(comodel_name="res.users", string="Salesperson", default=lambda self: self.env.user)
    offer_ids = fields.One2many(comodel_name='estate.property.offer', inverse_name="property_id", string="Offers")
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(string="No of Bedrooms", default=2.00)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Number of Facades")
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")
    total_area = fields.Integer(compute="_compute_total_area")
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
        ],
        default='new', required=True, copy=False
    )

    @api.depends('garden_area', 'living_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area
