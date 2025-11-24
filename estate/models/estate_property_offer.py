from odoo import models, fields, api, exceptions


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate properties Offers"
    _order = "price desc"
    price = fields.Float('Price')
    status = fields.Selection(
        string='Status',
        default='new',
        copy=False,
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
            ('new', 'New')
        ])
    partner_id = fields.Many2one('res.partner', string='Buyer', required=True)
    property_id = fields.Many2one('estate.property', string='Estate Property', required=True)
    validity = fields.Integer('Validity', default=7)
    date_deadline = fields.Datetime('Deadline', compute='_compute_date_deadline', inverse='_inverse_date_deadline')
    property_type_id = fields.Many2one(related='property_id.property_type_id', store=True)
    _check_positive_price = models.Constraint(
        'CHECK(price >= 0)',
        'The price must be positive.',
    )

    @api.depends('validity', 'create_date')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = fields.Date.add(record.create_date, days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date).days

    def action_accept_offer(self):
        if any(record.status == 'accepted' for record in self.property_id.offer_ids):
            raise exceptions.UserError('An offer is already accepted for this property')
        for record in self:
            record.status = 'accepted'
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            record.property_id.state = 'offer_accepted'
        return True

    def action_refuse_offer(self):
        for record in self:
            if record.status == 'accepted':
                raise exceptions.UserError('You cant refuse an already accepted offer')
            record.status = 'refused'
        return True

    @api.model
    def create(self, vals):
        for val in vals:
            linked_property = self.env['estate.property'].browse(val['property_id'])
            if val['price'] < linked_property.best_price:
                raise exceptions.UserError("An offer with a higher price already exists")
            linked_property.state = 'offer_received'
        return super().create(vals)
