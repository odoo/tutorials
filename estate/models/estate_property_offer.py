from odoo import api, fields, models, exceptions, tools
from dateutil.relativedelta import relativedelta


class property_offer(models.Model):
    _name = "estate.property.offer"
    _description = "Model to modelize Offer for Properties"
    _order = "price DESC"

    price = fields.Float()
    status = fields.Selection(
        string='Status',
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        help="The Status of the offer"
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True, ondelete='cascade')
    validity = fields.Integer(default=7, string="Validity (days)")
    date_deadline = fields.Datetime(compute="_compute_deadline", inverse="_inverse_deadline", string="Deadline")
    property_type_id = fields.Many2one(related="property_id.property_type_id")

    _sql_constraints = [
        ('positive_price', 'CHECK(price >=0)', 'The Offer\'s price must be positive.')
    ]

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            record.date_deadline = (record.create_date if record.create_date else fields.date.today()) + relativedelta(days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            record.validity = (record.date_deadline.date() - (record.create_date if record.create_date else fields.date.today())).days

    def accept_offer(self):
        for record in self:
            if (record.property_id.has_accepted_offer()):
                raise exceptions.UserError("Only one Offer can be accepted")
            if (tools.float_utils.float_compare(record.property_id.expected_price * 90 / 100, record.price, 2) > 0):
                raise exceptions.ValidationError("You can't accept an offer lower than 90% of the selling price.")
            record.status = "accepted"
            record.property_id.selling_price = record.price
            record.property_id.state = 'offer_accepted'
            record.property_id.buyer_id = record.partner_id
        return True

    def decline_offer(self):
        for record in self:
            record.status = "refused"
        return True

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_offering = self.env['estate.property'].browse(vals['property_id'])
            if vals['price'] < property_offering.best_offer_price:
                raise exceptions.ValidationError("You can't create an offer with a lower price than already existing offer.")
            property_offering.state = "offer_received"
        return super().create(vals_list)
