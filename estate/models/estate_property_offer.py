from odoo import api, fields, models
from datetime import date, timedelta
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Define an offer for a given property'
    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)', "An offer price must be strictly positive")
    ]
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        copy=False,
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused')
        ]
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7, string="Validity (days)")
    date_deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_deadline", string="Deadline")
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)

    @api.depends('validity')
    def _compute_deadline(self):
        for record in self:
            if not record.create_date:
                record.create_date = date.today()
            record.date_deadline = record.create_date + timedelta(days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days

    @api.model
    def create(self, vals):
        property_id = self.env['estate.property'].browse(vals['property_id'])
        if vals['price'] < property_id.best_price:
            raise UserError("Your offer is too low. You cannot create an offer lower than the best offer.")
        property_id.state = 'offer_received'
        return super().create(vals)

    def action_accept_offer(self):
        for record in self:
            if 'accepted' in record.mapped("property_id.offer_ids.status"):
                raise UserError("Multiple offers can't be accepted.")
            record.status = 'accepted'
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            record.property_id.state = 'offer_accepted'
        return True

    def action_refuse_offer(self):
        for record in self:
            if record.status == 'accepted':
                record.property_id.buyer_id = False
                record.property_id.selling_price = False
            record.status = 'refused'
        return True
