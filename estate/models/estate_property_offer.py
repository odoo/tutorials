from odoo import models, fields

class EstatePropertyOffer(models.Model):
    _name = "estate_property_offer_model"

    price = fields.Float(required=True)
    status = fields.Selection([('accepted', 'Accepted'), ('refused', 'Refused')], string="Offer Status")
    partner_id = fields.Many2one(comodel_name="res.partner", string="Partner")
    property_id = fields.Many2one(comodel_name="estate_property_model", string="Estate Property")