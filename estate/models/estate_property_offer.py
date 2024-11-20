# -*- coding: utf-8 -*-
# licence

from odoo import fields, models

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property offers"
    # _order = "sequence"

    name = fields.Char('Name', required=False, default="- no name -")
    price = fields.Float('Offer price', required=True)
    # Reserved
    state = fields.Selection(string="Status", selection=[('new', 'New'), ('accepted', 'Accepted'), ('refused', 'Refused')], default='new', required=True)
    # Relational
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)