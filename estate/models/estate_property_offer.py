from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "Real Estate Property Offer"

    _offer_price = models.Constraint('CHECK(price>0)', 'Offer Price must be positive')

    price = fields.Float(string="Price", default=1.0)
    status = fields.Selection(
        selection=[
            ('new', "New"),
            ('offer_accepted', "Offer Accepted"),
            ('offer_rejected', "Offer Rejected"),
        ],
        string="Status",
        default='new',
    )
    partner_id = fields.Many2one(
        "res.partner",
        string="Partner",
        required=True,
    )
    property_id = fields.Many2one(
        "estate.property",
        string="Property",
        required=True,
    )
    validity = fields.Integer(string="Validity")
    date_deadline = fields.Date(
        string='Date Deadline',
        default=fields.Date.context_today,
        compute='_compute_date_deadline',
        inverse='_inverse_date_deadline',
    )

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for rec in self:
            if rec.create_date:
                rec.date_deadline = rec.create_date.date() + timedelta(days=rec.validity)
            else:
                rec.date_deadline = fields.Date.today() + timedelta(days=rec.validity)

    def _inverse_date_deadline(self):
        for rec in self:
            if rec.create_date:
                rec.validity = (rec.date_deadline - rec.create_date.date()).days
            else:
                rec.validity = (rec.date_deadline - fields.Date.today()).days

    def accept(self):
        for rec in self:
            if rec.property_id.status == 'accepted':
                return

            other_offers = self.search([
                ('property_id', '=', rec.property_id.id),
                ('status', '=', 'new'),
                ('id', '!=', rec.id),
            ])
            other_offers.write({'status': 'offer_rejected'})

            rec.status = 'offer_accepted'

            rec.property_id.write({
                'selling_price': rec.price,
                'buyer_id': rec.partner_id.id,
                'status': 'sold',
            })

    def reject(self):
        for rec in self:
            rec.status = 'offer_rejected'

            rec.property_id.write({
                'selling_price': 0,
            })

    def reset(self):
        for rec in self:

            self.search([
                ('property_id', '=', rec.property_id.id),
            ]).write({
                'status': 'new',
            })

            rec.property_id.write({
                'selling_price': 0,
                'buyer_id': False,
                'status': 'new',
            })

    # @api.constrains('price')
    # def check_price(self):
    #     for rec in self:
    #         if rec.price <= 0:
    #             message = "Price needs to positive only"
    #             raise ValidationError(message)
    