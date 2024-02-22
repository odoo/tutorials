from odoo import models, fields, api, exceptions


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        copy=False,
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused')
        ]
    )
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute="_compute_deadline_date", inverse="_inverse_deadline_date", string="Deadline")

    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)

    property_type_id = fields.Many2one("estate.property.type",
                                       related="property_id.property_type_id", store=True)

    _sql_constraints = [
        ('check_positive_price', 'CHECK(price > 0)',
         'The offer price should be positive.'),
    ]

    @api.depends("validity", "create_date")
    def _compute_deadline_date(self):
        for record in self:
            initial_date = record.create_date if record.create_date else fields.Date.today()
            record.date_deadline = fields.Date.add(
                initial_date, days=record.validity)

    def _inverse_deadline_date(self):
        for record in self:
            initial_date = record.create_date if record.create_date else fields.Date.today()
            initial_date = fields.Date.to_date(initial_date)
            record.validity = (record.date_deadline - initial_date).days

    def action_accept(self):
        for record in self:
            if record.property_id.buyer_id:
                raise exceptions.UserError(
                    message="This property has as accepted offer!")

            record.property_id.buyer_id = record.partner_id
            record.property_id.state = 'accepted'
            record.status = 'accepted'
            record.property_id.selling_price = record.price
        return True

    def action_reject(self):
        for record in self:
            if record.property_id.buyer_id == record.partner_id and record.property_id.selling_price == record.price:
                raise exceptions.UserError(
                    "An accepted offer can not be rejected back!")
            record.status = 'refused'
        return True
