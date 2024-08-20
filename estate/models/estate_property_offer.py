import datetime

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class EstatePropertyType(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"
    _sql_constraints = [
        ('check_price', 'CHECK(price >= 0)',
         'The price should be positive'),
    ]

    price = fields.Float()
    status = fields.Selection(copy=False, selection=[("accepted", "Accepted"), ("refused", "Refused")])
    partner_id = fields.Many2one("res.partner", required=True, string="Partner")
    property_id = fields.Many2one("estate.property", required=True, string="Property")
    validity = fields.Integer(default=7, string="Validity (days)")

    property_type_id = fields.Many2one("estate.property.type", string="Property Type",
                                       related="property_id.property_type_id", store=True)

    # computed fields
    date_deadline = fields.Date(compute='_compute_date_deadline', inverse='_inverse_date_deadline', string="Deadline")

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = datetime.datetime.today() + datetime.timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - datetime.date.today()).days

    def confirm_offer(self):
        for offer in self:
            if offer.status != "accepted":
                offer.status = "accepted"
                offer.property_id.state = "offer_accepted"
                offer.property_id.selling_price = offer.price
                offer.property_id.buyer_id = offer.partner_id

    def cancel_offer(self):
        for offer in self:
            if offer.status != "refused":
                offer.status = "refused"
                offer.property_id.selling_price = 0
                offer.property_id.buyer_id = ""

    @api.model
    def create(self, vals):
        property_id = self.env['estate.property'].browse(vals['property_id'])
        if vals['price'] < min(property_id.offer_ids.mapped('price')):
            raise UserError(_("The price should be higher than the others."))
        property_id.state = "offer_received"
        return super().create(vals)
