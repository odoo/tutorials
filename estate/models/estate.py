from odoo import api, exceptions, fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Brand new Model"

    name = fields.Char(required=True, default="Unknown")
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
    garden_orientation = fields.Selection(selection=[
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')
    ])
    active = fields.Boolean(default=False)
    state = fields.Selection(selection=[
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('canceled', 'Canceled')
    ], required=True, copy=False, default='new')
    property_type_id = fields.Many2one("estate.property.type", string="Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson_id = fields.Many2one("res.users", string="Sales Person", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many(comodel_name="estate.property.offer", inverse_name="property_id", string="Offers")
    total_area = fields.Float(compute="_compute_area")
    best_price = fields.Float(compute="_compute_best_price")

    @api.depends("garden_area", "living_area")
    def _compute_area(self):
        for property in self:
            property.total_area = property.garden_area + property.living_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for property in self:
            if (len(property.offer_ids) > 0):
                property.best_price = max(property.offer_ids.mapped("price"))
            else:
                property.best_price = 0

    @api.onchange("garden")
    def _onchange_garden(self):
        if (self.garden):
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = ""

    def estate_cancel(self):
        for property in self:
            if (property.state != "sold"):
                property.state = "canceled"
            else:
                raise exceptions.UserError("Cancelled property can not be sold.")
        return True

    def estate_sold(self):
        for property in self:
            if (property.state != "canceled"):
                property.state = "sold"
            else:
                raise exceptions.UserError("Sold property can not be cancel")
        return True
    