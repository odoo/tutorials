from odoo import models, fields, api
from odoo.exceptions import UserError



class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "this is defind the offer of properties"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")], copy=False
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    property_type_id = fields.Many2one(
        related="property_id.property_type_id", store=True
    )

    validity = fields.Integer("Offer Validity", default=7)
    date_deadline = fields.Date(
        "Deadline", compute="_compute_deadline", inverse="_compute_validity"
    )

    _check_offer_price_positive = models.Constraint(
        "CHECK(price>0)", "The offer price must be strictly positive"
    )

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.add(
                record.create_date or fields.Date.today(), days=record.validity
            )

    def _compute_validity(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days

    def action_accept_offer(self):
        for record in self:
            if record.property_id.state == "offer_accepted":
                raise UserError(message="one offer is already accpted")
            else:
                record.status = "accepted"
                record.property_id.selling_price = record.price
                record.property_id.buyer_id = record.partner_id
                record.property_id.state = "offer_accepted"
                for offer in record.property_id.offer_property_ids:
                    if record.id != offer.id:
                        offer.status = "refused"
        return True

    def action_refused_offer(self):
        for record in self:
            record.status = "refused"
        return True

    @api.model
    def create(self,vals):
      for val in vals:
         x=self.env['estate.property'].browse(val['property_id'])
         if x.offer_property_ids.filtered(lambda r : r.price > val['price']):
            raise UserError("This offer's price is less than existing offer's price")
         x.state='offer_received'

      return  super().create(vals)



# vals[0].get('xyz')
# vals[0]['xyz']
