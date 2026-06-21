from odoo import models, fields

class EstatePropertyOffer(models.Model):
    _name = "estate_property_offer_model"

    price = fields.Float(required=True)
    status = fields.Selection([('accepted', 'Accepted'), ('refused', 'Refused')], string="Offer Status")
    partner_id = fields.Many2one(comodel_name="res.partner", string="Partner")
    property_id = fields.Many2one(comodel_name="estate_property_model", string="Estate Property")

    def action_accept_offer(self):
        self.status = "accepted"
        return True

    def action_refuse_offer(self):
        self.status = "refused"
        return True