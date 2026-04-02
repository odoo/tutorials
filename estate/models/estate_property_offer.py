from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Offer"

    price = fields.Float(string='Price')
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused')
    ], copy=False)
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_deadline_method", inverse="_inverse_deadline_method")

    _check_offer_price = models.Constraint(
        'CHECK(price >= 1)',
        'The offer price must be strictly positive'
    )

    @api.depends("create_date", "validity")
    def _compute_deadline_method(self):
        for rec in self:
            create_date = rec.create_date.date() if rec.create_date else fields.Date.today()
            rec.date_deadline = create_date + relativedelta(days=rec.validity)

    def _inverse_deadline_method(self):
        for rec in self:
            create_date = rec.create_date.date() if rec.create_date else fields.Date.today()
            rec.validity = relativedelta(rec.date_deadline, create_date).days

    def action_accept_offer(self):
        for rec in self:
            if any(i.status == "accepted" for i in rec.property_id.offer_ids):
                raise UserError("Offer already accepted for given property.")

            rec.status = "accepted"
            rec.property_id.buyer_id = rec.partner_id.id
            rec.property_id.selling_price = rec.price
            rec.property_id.state = "offer_accepted"
        return True

    def action_refuse_offer(self):
        for rec in self:
            rec.status = "refused"
        return True
