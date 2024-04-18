from odoo import api, fields, models
from odoo.tools import date_utils
from odoo.exceptions import UserError

class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "describes an offer made on a property"
    _order = "price desc"
    _sql_constraints = [
         ('check_price', 'CHECK(price > 0)',
         'An offer price must be strictly positive.')
    ]

    price = fields.Float()
    status = fields.Selection(
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused')],
        copy=False
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)
    validity = fields.Integer()
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline", string="Deadline")

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            if (not record.create_date):    # When creating an offer create_date is not defined yet
                record.date_deadline = date_utils.add(fields.Date.today(), days=record.validity)
                continue
            record.date_deadline = date_utils.add(record.create_date, days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if (not record.create_date):    # When creating an offer create_date is not defined yet
                record.validity = (record.date_deadline - fields.Date.today()).days
                continue
            record.validity = (record.date_deadline - record.create_date.date()).days

    def action_confirm_offer(self):
        if "accepted" in self.mapped("property_id.offer_ids.status"):
            raise UserError("Another offer is accepted.")
        self.status = "accepted"
        self.property_id.buyer = self.partner_id
        self.property_id.selling_price = self.price
        self.property_id.state = "offer_accepted"
        return True

    def action_refuse_offer(self):
        for record in self:
            if (record.status == "accepted"):
                self.property_id.state = "offer_received"
            record.status = "refused"
            record.property_id.buyer = False
            record.property_id.selling_price = False
        return True

    @api.model
    def create(self, vals):
        property_id = self.env['estate.property'].browse(vals['property_id'])
        if vals['price'] < property_id.best_price:
            raise UserError("An offer cannot be created if another offer has a higher price.")
        property_id.state = 'offer_received'
        return super().create(vals)
