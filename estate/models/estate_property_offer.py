from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import ValidationError, UserError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "All property offer"
    _order = 'price desc'

    price = fields.Float()

    property_id = fields.Many2one('estate.property', string="property", required=True, readonly=True)
    partner_id = fields.Many2one('res.partner', string="partner", required=True)
    property_type_id = fields.Many2one(related='property_id.property_type_id')

    status = fields.Selection(
        copy=False,
        selection=[('accepted', "Accepted"), ('refused', "Refused")]
    )

    validity = fields.Integer(default=7)

    date_deadline = fields.Date(compute='_compute_deadline', inverse='_inverse_deadline', string="Deadline")

    _check_price = models.Constraint(
        'CHECK(price > 0)',
        "The price must be strictly positive.",
    )

    @api.depends('validity')
    def _compute_deadline(self):
        for offer in self:
            offer.date_deadline = fields.Date.today() + relativedelta(days=offer.validity)

    def _inverse_deadline(self):
        for offer in self:
            offer.validity = relativedelta(offer.date_deadline, fields.Date.today()).days

    def offer_cancel(self):
        for offer in self:
            if offer.status == 'accepted':
                raise UserError(self.env._("You can not cancel an accepted offer"))
            else:
                offer.status = 'refused'
        return True

    def offer_accept(self):
        for offer in self:
            if offer.property_id.state != 'accepted':
                offer.status = 'accepted'
                offer.property_id.accepted_offer(offer)
            else:
                raise UserError(self.env._("There is already an accepted offer for %s.", offer.property_id.name))

        return True

    @api.model
    def create(self, vals_list):
        for vals in vals_list:
            property = self.env['estate.property'].browse(vals['property_id'])
            if vals['price'] < property.best_price:
                raise ValidationError(self.env._("Can not create an offer lower than an existing offer"))
            property.set_received()
        return super().create(vals_list)
