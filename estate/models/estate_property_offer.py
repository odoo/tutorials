from odoo import fields, models, api, exceptions


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "Estate property offers"
    _order = 'price desc'

    price = fields.Float()
    _check_price = models.Constraint(
        'CHECK(price > 0)',
        "The price of an offer must be positive.",
    )
    status = fields.Selection(
        selection=[('accepted', "Accepted"), ('refused', "Refused")],
        copy=False
    )
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    property_id = fields.Many2one('estate.property', string="Property", required=True)
    property_type_id = fields.Many2one(related='property_id.property_type_id')

    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute='_compute_deadline', inverse='_inverse_deadline', string="Deadline")

    @api.depends('create_date', 'validity')
    def _compute_deadline(self):
        for record in self:
            if (record.create_date):
                record.date_deadline = fields.Date.add(record.create_date, days=record.validity)
            else:
                record.date_deadline = fields.Date.add(fields.Date.today(), days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - fields.Date.to_date(record.create_date)).days

    def action_accept(self):
        for record in self:
            for offer in record.property_id.property_offer_ids:
                offer.status = 'refused'
            record.status = 'accepted'
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
        return True

    def action_refuse(self):
        for record in self:
            record.status = 'refused'
        return True

    @api.model
    def create(self, vals_list):
        for vals in vals_list:
            propertyId = self.env['estate.property'].browse(vals['property_id'])
            curPrice = vals['price']
            if propertyId.best_price > curPrice:
                raise exceptions.UserError(f"Cannot create an offer with a lower price than the best offer:{propertyId.best_price}")
            propertyId.state = 'offer_received'
        return super().create(vals_list)
