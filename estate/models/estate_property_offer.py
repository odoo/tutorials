from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "estate property offer"
    _order = "price desc"

    _check_offer_price = models.Constraint(
        "CHECK(price > 0)",
        "The offer price must be strictly positive.",
    )

    price = fields.Float()
    status = fields.Selection(
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
        copy=False,
    )

    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    property_type_id = fields.Many2one(related="property_id.property_type_id", string="property type")
    validity = fields.Integer(default=7, string="Validity(days)")
    date_deadline = fields.Date(string="Deadline Date", compute="_compute_deadline", inverse="_inverse_deadline")

    @api.depends("validity")
    def _compute_deadline(self):
        for offer in self:
            default_creation_date = offer.create_date or fields.Date.today()
            offer.date_deadline = relativedelta(days=offer.validity) + default_creation_date

    def _inverse_deadline(self):
        for offer in self:
            default_creation_date = offer.create_date or fields.Date.today()
            offer.validity = (offer.date_deadline - fields.Date.to_date(default_creation_date)).days

    def action_accept(self):
        for offer in self:
            if offer.property_id.buyer_id:
                raise ValidationError("Sorry, but we already accepted an offer for this property")
            else:
                offer.status = 'accepted'
                offer.property_id.selling_price = offer.price
                offer.property_id.state = 'offer_accepted'
                offer.property_id.buyer_id = offer.partner_id
        return True

    def action_refuse(self):
        for offer in self:
            offer.status = 'refused'
        return True

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property = self.env['estate.property'].browse(vals['property_id'])
            if property.state == 'new':
                property.state = 'offer_received'

            if vals['price'] < property.best_offer:
                raise UserError("Offer must be higher or equal than %d" % property.best_offer)

        return super().create(vals_list)
