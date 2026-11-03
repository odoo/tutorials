from datetime import datetime, time
from dateutil.relativedelta import relativedelta
from odoo import fields, models, api
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"
    _order = "price desc"

    _postif_price = models.Constraint("CHECK (price > 0)", "A price can't be negatif")

    price = fields.Float(string="Price", required=True)
    status = fields.Selection(copy=False, selection=[
                                            ("accepted", "Accepted"),
                                            ("refused", "Refused")])

    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', ondelete='cascade', required=True)
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)
    validity = fields.Integer(string="Validity Duration", default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    def accept_offer(self):
        for record in self:
            if (record.property_id.selling_price == 0):
                record.status = "accepted"
                record.property_id.buyer_id = record.partner_id
                record.property_id.selling_price = record.price
                record.property_id.state = 'offer_accepted'
        return True

    def refused_offer(self):
        for record in self:
            record.status = "refused"
        return True

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            if (isinstance(record.create_date, bool)):
                record.date_deadline = fields.Datetime.now() + relativedelta(days=record.validity)
                return
            record.date_deadline = record.create_date + relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (datetime.combine(record.date_deadline, time()) - record.create_date).days

    @api.model
    def create(self, vals_list):
        property_ids = (val['property_id'] for val in vals_list)
        property = self.env['estate.property'].browse(property_ids)
        print('-----------------------------------')
        print(property)
        for i, record in enumerate(vals_list):
            print('-----------------------------------')
            print(property[i].best_price)
            print(type(property[i].best_price))
            print('-----------------------------------')
            if (float_compare(record['price'], property[i].best_price, 2) == -1):
                raise UserError(self.env._("This offer is lower than what has already been offered."))
        return super().create(vals_list)
