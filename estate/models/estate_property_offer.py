# -*- coding: utf-8 -*-
from odoo import models, fields


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property offers for the estate"

    price = fields.Float()
    status = fields.Selection(
        string="Status",
        selection=[("accepted", "Accepted"), ("refused", "Refused"), ("pending", "Pending")],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", copy=False)
    property_id = fields.Many2one("estate.property", string="Property", copy=False)


