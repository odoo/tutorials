from odoo import models, fields, api

class EstateProperty(models.Model):
    _name = "estate_property"
    _description = "manage properties"

    name = fields.Char(string="Name", required=True, default="Unknown")
    description = fields.Text(string="Description")
    postcode = fields.Char(string="PostCode")
    date_availability = fields.Date(string="Availability", copy=False, default=fields.Datetime.add(fields.Datetime.today(), months=3))
    expected_price = fields.Float(string="Excepted price", required=True)
    selling_price = fields.Float(string="Selling price", readonly=True, copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living area")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden area")
    garden_orentation = fields.Selection(string="Garden orientation", selection=[('north', 'North'),('south', 'South'), ('ouest', 'West'), ('east', 'East')])
    active = fields.Boolean(default=True)
    states = fields.Selection(string="State", selection=[('new','New'),('offer_received','Offre Received'),('offer_accepted','Offer Accepted'),('sold','Sold'),('cancelled','Cancelled')])

    tags_ids = fields.Many2many("estate_property_tags", string="Tags")
    salesman_id = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    estate_property_type = fields.Many2one("estate_property_type", string="Property Type")
    offer_ids = fields.One2many(comodel_name="estate_property_offer", inverse_name="property_id", string="Offers")

    total_area = fields.Float(compute="_compute_area", string="Total area")
    best_price = fields.Float(compute="_compute_best_price", string="Best Offer")

    @api.depends("garden_area","living_area")
    def _compute_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            prices = record.offer_ids.mapped('price')
            record.best_price = max(prices) if prices else 0.0

    @api.onchange("garden")
    def _update_garden_values(self):
        if self.garden is True:
            self.garden_area = 20
            self.garden_orentation = 'north'
        else:
            self.garden_area = 0
            self.garden_orentation = ''



class EstatePropertyType(models.Model):
    _name ="estate_property_type"
    _description="property type"

    name = fields.Char(string="Name", required=True)

class EstatePropertyTags(models.Model):
    _name ="estate_property_tags"
    _description="property tags"

    name = fields.Char(string ="Name", required=True)

class EstatePropertyOffer(models.Model):
    _name = "estate_property_offer"
    _description = "property offers"

    price = fields.Float(string="Price")
    status = fields.Selection(string="Status", selection=[('accepted', 'Accepted'),('refused', 'Refused')])
    partner_id = fields.Many2one("res.partner", string="Acheteur", required=True)
    property_id = fields.Many2one("estate_property", string="Property", required=True)
    validity = fields.Integer(string="Validity", compute="_compute_validity", inverse="_inverse_validty")
    date_deadline = fields.Date(string="Deadline")

    @api.depends("date_deadline")
    def _compute_validity(self):
        for record in self:
            if record.create_date and record.date_deadline:
                delta = record.date_deadline - record.create_date.date()
                record.validity = int(delta.days)

    def _inverse_validty(self):
        for record in self:
            if record.create_date and record.validity:
                record.date_deadline = fields.Datetime.add(record.create_date, days=record.validity)