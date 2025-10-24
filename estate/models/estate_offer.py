from odoo import models, fields, api


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate offers"
    _order = "price desc"

    price = fields.Float(required=True)
    status = fields.Selection(
        selection=[
            ('new', 'New'),
            ('refused', 'Refused'),
            ('accepted', 'Accepted')
        ],
        default="new",
        copy=False
    )
    validity = fields.Integer(default=7)
    create_date = fields.Date(default=lambda self: fields.Date.today(), readonly=True)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_validity")

    # relations
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True, ondelete="cascade")
    property_type_id = fields.Many2one(
        related="property_id.property_type_id",
        store=True,
    )
    
    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.add(record.create_date, days=record.validity)

    @api.depends("date_deadline")
    def _inverse_validity(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date).days

    def action_accept(self):
        for record in self:
            record.status = 'accepted'
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            record.property_id.state = 'accepted'

        return True

    def action_refuse(self):
        for record in self:
            record.status = 'refused'
        return True
    
    @api.model
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
