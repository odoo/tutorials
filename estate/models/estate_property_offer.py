from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Offer"
    _order = "price desc"

    price = fields.Float(string='Price')
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused')
    ], copy=False)
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline")
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)

    _check_offer_price = models.Constraint(
        'CHECK(price >= 1)',
        'The offer price must be strictly positive'
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for rec in self:
            create_date = rec.create_date.date() if rec.create_date else fields.Date.today()
            rec.date_deadline = create_date + relativedelta(days=rec.validity)

    def _inverse_date_deadline(self):
        for rec in self:
            create_date = rec.create_date.date() if rec.create_date else fields.Date.today()
            rec.validity = relativedelta(rec.date_deadline, create_date).days

    @api.model_create_multi
    def create(self, vals_list):
        for rec in vals_list:
            property_rec = self.env['estate.property'].browse(rec.get('property_id'))
            if rec.get('price') < property_rec.best_price:
                raise UserError(_("The offer must be higher than the existing offer."))
            property_rec.state = "offer_received"
        return super().create(vals_list)

    def action_accept_offer(self):
        for rec in self:
            if any(i.status == "accepted" for i in rec.property_id.offer_ids):
                raise UserError(_("Offer already accepted for given property."))
            rec.status = "accepted"
            rec.property_id.write({
                'buyer_id': rec.partner_id.id,
                'selling_price': rec.price,
                'state': 'offer_accepted'
            })
        other_offers = self.property_id.offer_ids.filtered(lambda o: o.status != 'accepted')
        other_offers.write({'status': 'refused'})
        return True

    def action_refuse_offer(self):
        for rec in self:
            rec.status = "refused"
        return True
