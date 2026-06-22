from odoo import models, fields

class EstatePropertyOffer(models.Model):
    _name = "estate_property_offer_model"
    _order = "price desc"

    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")

    price = fields.Float(required=True)
    status = fields.Selection([('recieved', 'Recieved'), ('accepted', 'Accepted'), ('refused', 'Refused')], string="Offer Status", default="recieved")
    partner_id = fields.Many2one(comodel_name="res.partner", string="Partner")
    property_id = fields.Many2one(comodel_name="estate_property_model", string="Estate Property")

    def action_accept_offer(self):
        self.status = "accepted"
        return True

    def action_refuse_offer(self):
        self.status = "refused"
        return True