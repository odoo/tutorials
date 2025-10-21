from odoo import models, fields, api, exceptions


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Properties"

    ####################################################
    # FIELDS DECLARATION
    ####################################################

    name = fields.Char(
        string='Title',
        required=True,
        default="My new house"
    )
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        string='Available From',
        default=fields.Date.add(fields.Date.today(), months=3),
        copy=False
    )
    expected_price = fields.Float(string='Expected price', required=True)
    selling_price = fields.Float(
        readonly=True,
        copy=False
    )
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string='Living Area (sqm)')
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string='Garden Area (sqm)')
    garden_orientation = fields.Selection(
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')]
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('canceled', 'Canceled')],
        default='new'
    )
    property_type_id = fields.Many2one("estate.property.type")
    partner_id = fields.Many2one("res.partner", string="Buyer")
    user_id = fields.Many2one(
        "res.users",
        string="Salesperson",
        default=lambda self: self.env.user
    )
    tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many(
        "estate.property.offer",
        "property_id"
    )
    total_area = fields.Float(compute="_compute_total_area")
    best_offer = fields.Float(compute="_compute_best_price")

    ####################################################
    # FUNCTIONS DECLARATION
    ####################################################

    def cancel_property_button(self):
        for record in self:
            if record.state != "sold":
                record.state = "canceled"
            else:
                raise exceptions.UserError("Sold properties cannot be canceled")
        return True

    def sold_property_button(self):
        for record in self:
            if record.state != "canceled":
                record.state = "sold"
            else:
                raise exceptions.UserError("Canceled properties cannot be sold")
        return True

    @api.depends("garden_area", "living_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_offer = max(record.offer_ids.mapped('price')) if record.offer_ids else 0

    @api.onchange("garden")
    def _onchange_garden(self):
        self.garden_orientation = "%s" % ("north" if self.garden else "")
        self.garden_area = "%s" % (10 if self.garden else "")
