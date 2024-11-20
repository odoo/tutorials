# -*- coding: utf-8 -*-
# licence

from odoo import fields, models

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate properties"
    # _order = "sequence"

    name = fields.Char('Title', required=True, translate=True)
    description = fields.Text('Property description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Date of availability', default=fields.Date.add(fields.Date.today(), days=30), copy=False)
    expected_price = fields.Float('Expected price', required=True)
    selling_price = fields.Float('Selling price', readonly=True, copy=False)
    bedrooms = fields.Integer('No. of bedrooms', default=2)
    living_area = fields.Integer('Living area surface')
    facades = fields.Integer('No. of facades')
    garage = fields.Boolean('Has a garage')
    garden = fields.Boolean('Has a garden')
    garden_area = fields.Integer('Gargen area surface')
    garden_orientation = fields.Selection(string='Garden orientation', selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
    # Reserved
    active = fields.Boolean('Active', default=True)
    state = fields.Selection(string='State', selection=[('new', 'New'), ('recieved', 'Offer Received'),
                                                        ('accepted', 'Offer Accepted'), ('sold', 'Sold'),
                                                        ('cancelled', 'Cancelled')], required=True, copy=False, default='new')
    # Relational
    property_type_id = fields.Many2one("estate.property.type", string="Type")
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    buyer_id = fields.Many2one("res.partner", string="Buyer")
    salesperson_id = fields.Many2one("res.users", string="Salesperson") #, default=self.env.user) # <-- apparently this is not how it works