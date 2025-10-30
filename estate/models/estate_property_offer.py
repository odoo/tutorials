from datetime import timedelta
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "estate property OFFER created"
    _order = "price desc"
    _sql_constraints = [
        ('offer_price_positive', 'CHECK(price>=0)', 'The offer price should be positive.')
    ]

    price = fields.Float()
    status = fields.Selection(
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", string="Partner", index=True, required=True, default=lambda self: self.env.user.partner_id.id)
    property_id = fields.Many2one("estate.property", index=True, required=True)
    property_type_id = fields.Many2one('estate.property.type', string="property type", related="property_id.property_type_id", store=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        store=True
    )

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                create_date = record.create_date.date()
            else:
                create_date = fields.Date.today()
            record.date_deadline = create_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date:
                create_date = record.create_date.date()
            else:
                create_date = fields.Date.today()
            if record.date_deadline:
                record.validity = (record.date_deadline - create_date).days

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_id = vals.get("property_id")
            price = vals.get("price", 0.0)
            if property_id:
                property_obj = self.env["estate.property"].browse(property_id)
                best_price = property_obj.best_offer or 0.0
                if price < best_price:
                    raise UserError(
                        "Offer price must be greater than or equal to the best offer price.")
        records = super().create(vals_list)
        for record in records:
            if record.partner_id:
                record.property_id.state = "Offer Received"
        return records

    def refuse_icon_action(self):
        for record in self:
            record.status = 'refused'

    def accept_icon_action(self):
        for record in self:
            if any(
                offer.status == 'accepted'
                for offer in record.property_id.offer_ids
            ):
                raise UserError("Only one offer can be accepted per property.")
            min_price = record.property_id.expected_price * 0.9
            if float_compare(record.price, min_price, precision_digits=2) < 0:
                raise ValidationError("Offer must be at least 90% of the expected price to be accepted.")

            record.status = 'accepted'
            record.property_id.state = 'Offer Accepted'
            other_offers = record.property_id.offer_ids - record
            other_offers.write({'status': 'refused'})
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
