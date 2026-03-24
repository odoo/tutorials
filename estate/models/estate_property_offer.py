from dateutil.relativedelta import relativedelta

from odoo import fields, models, api
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "Estate property offer"

    _order = 'price desc'

    price = fields.Float(required=True, string="Price")
    status = fields.Selection([
        ('accepted', "Accepted"), ('refused', "Refused"),
    ], copy=False, string="Status", readonly=True)
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    property_id = fields.Many2one('estate.property', string="Property", required=True)
    validity = fields.Integer(required=True, string="Validity", default=7)
    date_deadline = fields.Date(string="Deadline", compute='_compute_date_deadline', inverse='_inverse_date_deadline')
    available_for_offers = fields.Boolean(related='property_id.available_for_offers')
    property_type_id = fields.Many2one('estate.property.type', related='property_id.property_type_id', store=True)

    _check_price = models.Constraint(
        'CHECK (price > 0)',
        "The price must be greater than 0."
    )

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.today() + relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = relativedelta(record.date_deadline, (record.create_date if record.create_date else fields.Date.today())).days

    def action_mark_as_accepted(self):
        for record in self:
            if record.available_for_offers:
                record.status = 'accepted'
                record.property_id.compute_accepted_offer(record)
            else:
                raise UserError(self.env._("This offer cannot be accepted because the property is already sold or canceled or an offer has been accepted"))

        return True

    def action_mark_as_refused(self):
        for record in self:
            if record.available_for_offers:
                record.status = 'refused'
            else:
                raise UserError(self.env._("This offer cannot be accepted because the property is already sold or canceled or an offer has been accepted"))

        return True

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'property_id' not in vals:
                raise UserError(self.env._("You must select a property for the offer."))
            if 'price' not in vals:
                raise UserError(self.env._("You must set a price for the offer."))

            property = self.env['estate.property'].browse(vals['property_id'])

            if len(property.offer_ids.filtered(lambda offer: offer.price > vals['price'])) > 0:
                raise UserError(self.env._("Cannot create an offer with a lower amount than the other offers for this property."))

        offers = super().create(vals_list)

        for record in offers:
            record.property_id.compute_new_offer()

        return offers
