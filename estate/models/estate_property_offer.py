from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "Offers for real estate properties"
    _order = 'price desc'

    currency_id = fields.Many2one(
        "res.currency", string="Currency",
        default=lambda self: self.env.company.currency_id,
    )
    price = fields.Monetary(required=True, string="Price")
    status = fields.Selection(
        string="Status",
        selection=[
            ('accepted', "Accepted"),
            ('refused', "Refused")
        ],
        copy=False
    )
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    property_id = fields.Many2one('estate.property', string="Property", required=True)
    validity = fields.Integer(default=7, string="Validity (days)")
    date_deadline = fields.Date(compute='_compute_date_deadline', inverse='_inverse_date_deadline', string="Deadline", readonly=False)
    property_type_id = fields.Many2one(related="property_id.property_type_id", string="Property Type")

    _check_price = models.Constraint(
        'CHECK(price >= 0)',
        "The offer price should be positive."
    )

    @api.depends('create_date', 'validity')
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

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals['property_id']:
                property = self.env['estate.property'].browse(vals['property_id'])
                if property.currency_id.compare_amounts(vals['price'], property.best_price) <= 0:
                    raise UserError(self.env._("New offers should have a higher price."))
                property.state = 'offer_received'

        return super().create(vals_list)

    def accept_offer(self):
        for record in self:
            if any(status for status in record.property_id.offer_ids.mapped('status') if status == 'accepted'):
                raise UserError(self.env._("Only one offer can be accepted by property."))
            record.status = 'accepted'
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
            record.property_id.state = 'offer_accepted'
        return True

    def refuse_offer(self):
        for record in self:
            record.status = 'refused'
        return True
