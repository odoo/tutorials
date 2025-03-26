from odoo import api, exceptions, fields, models
from dateutil.relativedelta import relativedelta

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "My Estate Property Offer"
    _order = "price desc"

    price = fields.Float(string = "Price")
    sql_constraints = [
        ("check_price", "CHECK(price > 0)", "Offer price should be positive.")
    ]

    status = fields.Selection([('accept', 'Accept'), ('refused', 'Refused')], copy = False, string = "Status")
    partner_id = fields.Many2one('res.partner', string = "Partner", required = True)
    property_id = fields.Many2one('estate.property', string = 'Property', required = True)
    property_type_id = fields.Many2one(related = 'property_id.property_type_id')

    validity = fields.Integer(string = "Validity", default = 7)
    date_deadline = fields.Date(compute = "_compute_deadline", inverse = "_inverse_deadline", string = "Deadline")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'property_id' in vals:
                property = self.env['estate.property'].browse(vals['property_id'])
                if property.state == "new":
                    property.state = "received"
                if vals['price'] < property.best_price:
                    raise exceptions.ValidationError("Current offer price lower than existing offer prices.")
        return super(EstatePropertyOffer, self).create(vals_list)

    @api.depends("create_date", "validity")
    def _compute_deadline(self):
        for record in self:
            start_date = record.create_date.date() if record.create_date else fields.Date.today()
            record.date_deadline = start_date + relativedelta(days = record.validity)

    def _inverse_deadline(self):
        for record in self:
            timedelta = record.date_deadline - record.create_date.date()
            record.validity = timedelta.days

    def action_accept(self):
        for property in self:
            if property.property_id.state in ['new', 'received']:
                property.status = "accept"
                property.property_id.buyer = self.partner_id
                property.property_id.selling_price = self.price
                property.property_id.state = "accepted"
            else:
                raise exceptions.UserError("Cannot accept offer.")

    def action_refuse(self):
        for offer in self:
            offer.status = "refused"
