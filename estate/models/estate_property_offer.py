from odoo import api, exceptions, fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Listing of offers for a property"
    _check_price = models.Constraint('CHECK(price > 0)')
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(copy=False, selection=[("accepted", "Accepted"), ("rejected", "Rejected")])
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")
    property_type_id = fields.Many2one("estate.property.type", related="property_id.property_type_id", store=True)

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            if not record.create_date:
                record.date_deadline = fields.Date.add(fields.Date.today(), days=record.validity)
            else:
                record.date_deadline = fields.Date.add(record.create_date, days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if not record.create_date:
                record.validity = (record.date_deadline - fields.Date.today()).days
            else:
                record.validity = (record.date_deadline - fields.Date.to_date(record.create_date)).days

    def action_accept_offer(self):
        if self.property_id.state in {"sold", "offer accepted", "cancelled"}:
            raise exceptions.UserError(self.env._("Offers can no longer be accepted for this property."))
        else:
            self.status = "accepted"
            self.property_id.state = "offer accepted"
            self.property_id.selling_price = self.price
            self.property_id.buyer_id = self.partner_id
        return True

    def action_reject_offer(self):
        self.status = "rejected"
        return True

    @api.model
    def create(self, values):
        for val in values:
            target = self.env['estate.property'].browse(val['property_id'])
            if val['price'] < target.best_price:
                raise exceptions.UserError(self.env._("You cannot make an offer lower than the current best offer."))
            if target.state == 'new':
                target.state = 'offer received'
        return super().create(values)
