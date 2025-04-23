from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_round, float_compare
from odoo.exceptions import ValidationError


class EstateProperty(models.Model):
    _name = "estate_property"
    _description = "manage properties"
    _order = "id desc"

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
    states = fields.Selection(string="State", default='new', selection=[('new','New'),('offer_received','Offre Received'),('offer_accepted','Offer Accepted'),('sold','Sold'),('canceled','Canceled')])

    tags_ids = fields.Many2many("estate_property_tags", string="Tags")
    salesman_id = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    estate_property_type = fields.Many2one("estate_property_type", string="Property Type")
    offer_ids = fields.One2many(comodel_name="estate_property_offer", inverse_name="property_id", string="Offers")

    total_area = fields.Float(compute="_compute_area", string="Total area")
    best_price = fields.Float(compute="_compute_best_price", string="Best Offer")

    _sql_constraints = [
        ('check_price_positive', 'CHECK(expected_price >= 0)', 'The price should be higher than 0'),
        ('check_selling_price_positive', 'CHECK(selling_price >= 0)','The selling price should be higher than 0'),
        ('check_unique_name','UNIQUE(name)','The name of the property should be unique'),
    ]

    @api.ondelete(at_uninstall=False)
    def _unlink_if_states_match(self):
        for record in self:
            if record.states not in ['new', 'canceled']:
                raise UserError("You can't delete active properties")

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

    def mark_as_sold(self):
        for record in self:
            if record.states == "canceled":
                raise UserError("You can't set a canceled property to sold")
            else:
                record.states = "sold"

    def mark_as_canceled(self):
        for record in self:
            if record.states == "sold":
                raise UserError("You can't cancel a sold property")
            else:
                record.states = "canceled"

    @api.constrains('selling_price','expected_price')
    def _check_selling_price(self):
        for record in self:
            if record.expected_price != 0 :
                min_selling_price = record.expected_price * 0.9
                if float_compare(record.selling_price, min_selling_price,2) == -1 :
                    raise ValidationError("Selling price shoudn't be lower than 90% of expected price")

class EstatePropertyType(models.Model):
    _name ="estate_property_type"
    _description="property type"
    _order="sequence, name, id"

    name = fields.Char(string="Name", required=True)
    property_ids = fields.One2many("estate_property", "estate_property_type", string="Properties")
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
    
    offer_ids = fields.One2many(comodel_name='estate_property_offer',inverse_name='property_type_id',string="Related offers")
    offer_count = fields.Integer(compute='_compute_offer_count')

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

class EstatePropertyTags(models.Model):
    _name ="estate_property_tags"
    _description="property tags"
    _order="name asc"

    name = fields.Char(string ="Name", required=True)
    color = fields.Integer(string="Color")

    _sql_constraints = [
        ('check_unique_name','UNIQUE(name)','The name of the tag should be unique'),
    ]

class EstatePropertyOffer(models.Model):
    _name ="estate_property_offer"
    _description ="property offers"
    _order="price desc"

    price = fields.Float(string="Price")
    status = fields.Selection(string="Status", selection=[('accepted', 'Accepted'),('refused', 'Refused')])
    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)
    property_id = fields.Many2one("estate_property", string="Property", required=True)
    validity = fields.Integer(string="Validity", compute="_compute_validity", inverse="_inverse_validty")
    date_deadline = fields.Date(string="Deadline")
    
    property_type_id = fields.Many2one(related="property_id.estate_property_type", string="Property Type", store=True)

    _sql_constraints = [
        ('check_price_positive', 'CHECK(price > 0)', 'The price should be higher than 0'),
    ]

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

    def action_confirm(self):
        for record in self:
            if record.property_id.states == 'sold':
                raise UserError("You can't validate an offer for a sold property")
            else:
                record.property_id.buyer_id = record.partner_id
                record.property_id.states = 'sold'
                record.property_id.selling_price = record.price
                record.status = 'accepted'

    def action_close(self):
        for record in self:
            record.status = 'refused'
        
    @api.model_create_multi
    def create(self, vals_list):
        offers = super().create(vals_list)
        for offer in offers:
            property = offer.property_id
            if any(offer.price < existing_price for existing_price in property.offer_ids.mapped('price')):
                raise UserError("You can't create offer with a lower price than existing offer")
            else:
                property.states = 'offer_received'
        return offers