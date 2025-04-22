from odoo import models, fields

class EstateProperty(models.Model):
    _name = "estate_property"
    _description = "manage properties"

    name = fields.Char(string = "Name", required=True, default="Unknown")
    description = fields.Text(string = "Description")
    postcode = fields.Char(string = "PostCode")
    date_availability = fields.Date(string = "Availability", copy=False, default=fields.Datetime.add(fields.Datetime.today(), months=3))
    expected_price = fields.Float(string = "Excepted price", required=True)
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


class EstatePropertyType(models.Model):
    _name = "estate_property_type"
    _description= "property type"

    name = fields.Char(string = "Name", required=True)

class EstatePropertyTags(models.Model):
    _name = "estate_property_tags"
    _description= "property tags"

    name = fields.Char(string = "Name", required=True)


class EstatePropertyOffer(models.Model):
    _name = "estate_property_offer"
    _description = "property offers"

    price = fields.Float(string="Price")
    status = fields.Selection(string="Status", selection=[('accepted', 'Accepted'),('refused', 'Refused')])
    partner_id = fields.Many2one("res.partner", string="Acheteur", required=True)
    property_id = fields.Many2one("estate_property", string="Property", required=True)