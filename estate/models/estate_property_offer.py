from dateutil.relativedelta import relativedelta
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Real Estate Property Offer'
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection([('accepted', 'Accepted'), ('refused', 'Refused')], copy=False)
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(default=7, string="Validity (Days)")
    date_deadline = fields.Date(
        compute='_compute_date_deadline',
        inverse='_inverse_date_deadline',
        string="Deadline",
        store=True,
    )
    property_type_id = fields.Many2one(related='property_id.property_type_id', store=True)

    _sql_constraints = [(
        "estate_property_offer_check_price",
        "CHECK(price > 0)",
        "The offer price must be positive",
    ),]

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + relativedelta(days=record.validity)
            else:
                record.date_deadline = fields.Date.today() + relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - fields.Date.today()).days

    def action_estate_property_offer_accept(self):
        if self.status == 'accepted':
            raise ValidationError("This offer has already been accepted.")
        self.property_id.buyer_id = self.partner_id.id
        self.property_id.selling_price = self.price
        self.property_id.offer_ids.status = 'refused'  # Refuse all offers
        self.status = 'accepted'  # Accept this offer

    def action_estate_property_offer_refuse(self):
        if self.status == 'refused':
            raise ValidationError("This offer has already been refused.")
        self.property_id.buyer_id = False
        self.property_id.selling_price = 0
        self.status = 'refused'
