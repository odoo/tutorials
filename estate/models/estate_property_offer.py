from odoo import api, fields, models, exceptions


class PropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Property Offer'

    price = fields.Float()
    status = fields.Selection([("accepted", "Accepted"), ("refused", "Refused")], copy=False)
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer(string="Validity (days)", default=7,)
    date_deadline = fields.Date("Deadline", compute="_compute_deadline", inverse="_inverse_deadline")

    def _inverse_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - fields.Date.today()).days

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
           if record.create_date:
               record.date_deadline = fields.Date.add(record.create_date, days=record.validity)
           else:
               record.date_deadline = fields.Date.add(fields.Date.today(), days=record.validity)

    def accept_offer(self):
        for record in self:
            if record.property_id.offer_ids.mapped("status").count("accepted") >= 1:
                raise exceptions.UserError("More than one offer can't be accepted for the same property")
            record.status = "accepted"
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            record.property_id.status = "offer_accepted"
        return True

    def refuse_offer(self):
        for record in self:
            record.status = "refused"
        return True
