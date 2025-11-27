from odoo import api, fields, models, _
from odoo.tools import float_compare
from odoo.exceptions import UserError, ValidationError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate property offer"
    _order = "price desc"

    _check_offer_price = models.Constraint(
        'CHECK(price > 0)', 'Offer price must be strictly positive.'
    )

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records:
            if record.property_id.state == "new":
                record.property_id.state = "offer_received"
        ## Another way is to leave the super.create() at the end of the function and browse for the property by id
        return records

    price = fields.Float("Expected Price")
    status = fields.Selection(
        string="Status", selection=[("yes", "Accepted"), ("no", "Refused")], copy=False
    )
    validity = fields.Integer(default=7)
    offer_creation_date = fields.Date(default=fields.Date.today())
    deadline = fields.Date(
        "Offer Deadline", compute="_compute_deadline", inverse="_inverse_deadline",
    )

    partner_id = fields.Many2one(
        'res.partner',
        string='Buyer',
        ondelete='restrict',
        default=lambda self: self.env.user.partner_id,
        required=True,
    )
    property_id = fields.Many2one(
        'estate.property', string='Property', ondelete='cascade', required=True,
    )
    property_type_id = fields.Many2one(
        related='property_id.property_type_id', string='Property Type', store=True,
    )

    @api.depends("validity", "offer_creation_date")
    def _compute_deadline(self):
        for record in self:
            record.deadline = fields.Date.add(
                record.offer_creation_date, days=record.validity
            )

    def _inverse_deadline(self):
        for record in self:
            record.validity = (record.deadline - record.offer_creation_date).days

    def action_accept_offer(self):
        for record in self:
            for offer in record.property_id.offer_ids:
                if offer.status == "yes":
                    raise UserError(_("Already accepted an offer for this property."))
            if float_compare(record.price, 0.9 * record.property_id.expected_price, 2) < 0:
                raise ValidationError("Accepted offer price cannot be less than 90 percent of property price")
            record.status = "yes"
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            record.property_id.state = "offer_accepted"
        return True

    def action_reject_offer(self):
        self.status = 'no'
        self.property_id.write({'buyer_id': None, 'selling_price': 0})
        return True

    @api.constrains('price')
    def _check_offered_price(self):
        for record in self:
            if float_compare(record.price, 0.9 * record.property_id.expected_price, 2) < 0:
                raise ValidationError("Offer price cannot be less than 90 percent of property price")
            if float_compare(record.price, record.property_id.best_offer, 2) < 0:
                raise ValidationError(_("The offer must be higher than %s", str(record.property_id.best_offer)))
