from datetime import timedelta
from odoo import models, fields, api
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "price desc"

    price = fields.Float(string="Price", required=True)
    status = fields.Selection(
        [('accepted', 'Accepted'), ('refused', 'Refused')],
        string="Status",
        copy=False
    )
    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer(default=7, string="Validity (Days)")
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline", string="Deadline")

    _check_price = models.Constraint(
        'CHECK(price > 0)',
        'The offer price must be strictly positive'
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            base_date = record.create_date.date() if record.create_date else fields.Date.today()
            record.date_deadline = base_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            base_date = record.create_date.date() if record.create_date else fields.Date.today()
            if record.date_deadline:
                record.validity = (record.date_deadline - base_date).days

    def action_accept_offer(self):
        for record in self:
            if record.status == 'accepted':
                continue

            record.status = 'accepted'
            record.property_id.write({
                'selling_price': record.price,
                'buyer_id': record.partner_id.id,
                'state': 'offer_accepted'
            })

            record.property_id.offer_ids.filtered(lambda o: o.id != record.id).write({
                'status': 'refused'
            })
        return True

    def action_refuse_offer(self):
        for record in self:
            record.status = 'refused'
        return True

    @api.model
    def create(self, vals):
        if len(vals) > 0:
            property = self.env['estate.property'].browse(vals[0]['property_id'])
        for record in vals:
            if property.state == 'new':
                property.state = 'offer_received'
            if record['price'] < property.best_price:
                raise UserError("Offer must be higher or equal than %d" % property.best_price)
        return super().create(vals)

    @api.model
    def _cron_move_sold(self):
        expired_offers = self.search([
            ('status', '=', False),
            ('date_deadline', '<', fields.Date.today())
        ])
        expired_offers.write({'status': 'refused'})
