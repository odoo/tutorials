from odoo import fields, models, api, exceptions


def _is_valid_state(state):
    if state == 'sold':
        raise exceptions.UserError(message="Can't accept/reject offer on a sold property!!")
    elif state == 'cancelled':
        raise exceptions.UserError(message="Can't accept/reject offer on a cancelled property!!")


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    price = fields.Float()
    status = fields.Selection(copy=False, selection=[('accepted', 'Accepted'), ('refused', 'Refused')])
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for record in self:
            create_date = record.create_date or fields.Date.today()
            validity = record.validity or 0
            record.date_deadline = fields.Date.add(create_date, days=validity)

    def _inverse_date_deadline(self):
        for record in self:
            create_date = fields.Date.to_date(record.create_date or fields.Date.today())
            record.validity = (record.date_deadline - create_date).days

    def action_set_refused_status(self):
        for record in self:
            _is_valid_state(record.property_id.state)
            if record.property_id.buyer_id:
                raise exceptions.UserError(message="This property has a buyer already!")
            if record.status:
                raise exceptions.UserError(message="this offer had been dealt!")

            record.status = 'refused'
        return True

    def action_set_accepted_status(self):
        for record in self:
            _is_valid_state(record.property_id.state)
            if record.property_id.buyer_id:
                raise exceptions.UserError(message="This property has a buyer already!")
            if record.status:
                raise exceptions.UserError(message="this offer had been dealt!")
            record.property_id.buyer_id = record.partner_id
            record.property_id.state = 'offer_accepted'
            record.status = 'accepted'
            record.property_id.selling_price = record.price
        return True

    _sql_constraints = [
        ('check_positive_offer_price', 'CHECK(price > 0)', 'An offer price must be strictly positive.')
    ]
