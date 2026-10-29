from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools import float_compare


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"

    price = fields.Float(required=True)
    status = fields.Selection(selection=[('accepted', 'Accepted'), ('refused', 'Refused')], copy=False)
    partner_id = fields.Many2one("res.partner", required=True, string="Partner")
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(compute='_compute_date_deadline', inverse='_inverse_date_deadline')
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)

    _check_price = models.Constraint(
        'CHECK(price > 0)',
        'An offer price must be strictly positive.'
    )

    @api.depends('validity', 'create_date')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = fields.Date.add(record.create_date, days=record.validity)
            else:
                record.date_deadline = fields.Date.add(fields.Date.today(), days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date:
                record.validity = (record.date_deadline - record.create_date.date()).days
            else:
                record.validity = (record.date_deadline - fields.Date.today()).days

    def accept_offer(self):
        for offer in self.property_id.property_offer_ids:
            if offer.status == 'accepted':
                raise UserError(self.env._("An offer has already been accepted"))
        self.status = 'accepted'
        self.property_id.state = 'offer_accepted'
        self.property_id.buyer_id = self.partner_id
        self.property_id.selling_price = self.price
        return True

    def refuse_offer(self):
        self.status = 'refused'
        return True

    @api.model
    def create(self, vals):
        if float_compare(vals[0]["price"], self.env['estate.property'].browse(vals[0]['property_id']).best_price, precision_digits=2) < 0:
            raise UserError(self.env._("You cannot create an offer with a lower amount than an existing offer."))
        self.env['estate.property'].browse(vals[0]['property_id']).state = 'offer_received'
        return super().create(vals)
