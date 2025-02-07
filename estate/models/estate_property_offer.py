from dateutil.relativedelta import relativedelta

from odoo import models, fields, api


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"
    
    _sql_constraints = [
        (
            'positive_offer_price', 'CHECK(price > 0)', 'Offer price must be strictly positive'
        )
    ]
    
    price=fields.Float(string="Price")
    status=fields.Selection(selection=[("accepted", "Accepted"), ("refused", "Refused")], copy=False)
    partner_id=fields.Many2one(comodel_name="res.partner", required=True)
    property_id=fields.Many2one(comodel_name="estate.property", required=True, ondelete="cascade")
    validity=fields.Integer(string="Validity", default=7)
    date_deadline=fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")
    
    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date.date() + relativedelta(days=record.validity)
            else:
                record.date_deadline = fields.Date.today() + relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days
    
    def action_accept_offer(self):
        self.status = "accepted"
        self.property_id.state = "offer_accepted"
        self.property_id.selling_price = self.price
        self.property_id.buyer = self.partner_id
        return True

    def action_refuse_offer(self):
        self.status = "refused"
        return True
