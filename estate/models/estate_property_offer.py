from odoo import models, fields


class EstatePropertyOffer(models.Model):

    _name = "estate.property.offer"
    _description = "Estate property offer"

    price = fields.Float("Offer Price")
    status = fields.Selection(string="Status", copy=False, selection=[('accepted', 'Accepted'), ('refused', 'Refused')])
    partner = fields.Many2one(string="Buyer", comodel_name="res.partner",required=True)
    property = fields.Many2one(string="Property", comodel_name="estate.property", required=True)
