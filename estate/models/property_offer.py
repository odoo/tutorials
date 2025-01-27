from odoo import fields, models
from datetime import date, timedelta

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "reals estate properties offer"

    property_type_id= fields.Char('Property Offer ID')
    price = fields.Float('Le Prix')
    status = fields.Selection([("Accepted","Accepted"),("Refused","Refused")],copy=False)
    partner_id=fields.Many2one("res.partner",required=True)
    property_id=fields.Many2one("estate.property",required=True)

    # properties = fields.One2many("estate.property","property_type_id",string="properties")
