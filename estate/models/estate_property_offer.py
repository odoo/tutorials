from dateutil.relativedelta import relativedelta

from odoo import models, fields, api
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "Estate Property Offer"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused')
        ]
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    property_type_id = fields.Many2one(related="property_id.type_id", store=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_deadline")

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            default_creation_date = record.create_date or fields.Date.today()
            record.date_deadline = relativedelta(days=record.validity) + default_creation_date

    def _inverse_deadline(self):
        for record in self:
            default_creation_date = record.create_date or fields.Date.today()
            record.validity = (record.date_deadline - fields.Date.to_date(default_creation_date)).days

    def action_accept(self):
        for record in self:
            if record.property_id.buyer:
                raise UserError("Property already accepted")
            else:
                record.status = 'accepted'
                record.property_id.selling_price = record.price
                record.property_id.state = 'offer_accepted'
                record.property_id.buyer = record.partner_id

    def action_refuse(self):
        for record in self:
            if record.status == 'accepted':
                raise UserError("Property already accepted")
            else:
                record.status = 'refused'

    _check_offer_price = models.Constraint(
    'CHECK(price>=0)',
    'offer price must be positive',
    )

    @api.model
    def create(self, vals):
        for record in vals:
            property = self.env['estate.property'].browse(record['property_id'])
            if property.state == 'new':
                property.state = 'offer_received'
            if record['price'] < property.best_offer:
                raise UserError("Offer must be higher or equal than %d" % property.best_offer)
        return super().create(vals)
