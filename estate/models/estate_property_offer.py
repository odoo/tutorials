from odoo import models, api
from odoo.fields import Float, Selection, Integer, Date, Many2one
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate offers"
    _order = "price desc"

    price = Float(required=True)
    status = Selection(
        selection=[
            ('new', 'New'),
            ('refused', 'Refused'),
            ('accepted', 'Accepted')
        ],
        default="new",
        copy=False
    )
    validity = Integer(default=7)
    create_date = Date(default=lambda self: Date.today(), readonly=True)
    date_deadline = Date(compute="_compute_date_deadline", inverse="_inverse_validity")

    # relations
    partner_id = Many2one("res.partner", required=True)
    property_id = Many2one("estate.property", required=True, ondelete="cascade")
    property_type_id = Many2one(
        related="property_id.property_type_id",
        store=True,
    )

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = Date.add(record.create_date, days=record.validity)

    @api.depends("date_deadline")
    def _inverse_validity(self):
        for record in self:
            if record.date_deadline:
                record.validity = (record.date_deadline - record.create_date).days

    def action_accept(self):
        for record in self:
            record.status = 'accepted'
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            record.property_id.state = 'accepted'

        return True

    def action_refuse(self):
        self.status = 'refused'
        return True

    @api.model_create_multi
    def create(self, vals_list):

        for offer in self:
            if offer.price > vals_list.price:
                raise UserError('The offer price should be greater than those already received')

        res = super().create(vals_list)

        if res.property_id.state != 'received':
            res.property_id.state = 'received'

        return res

    _check_selling_price = models.Constraint(
        'CHECK(price > 0)',
        'The offer price should be strictly postitive',
    )
