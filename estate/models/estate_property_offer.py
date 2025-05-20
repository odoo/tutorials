from odoo import api, fields, models, exceptions, tools
from dateutil.relativedelta import relativedelta

class property_offer(models.Model):
    _name = "estate.property.offer"
    _description = "Model to modelize Offer for Properties"

    price = fields.Float()
    status= fields.Selection(
        string='Status',
        selection=[('accepted','Accepted'), ('refused','Refused')],
        help="The Status of the offer"
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity =  fields.Integer(default=0, string="Validity (days)")
    date_deadline = fields.Datetime(compute="_compute_deadline", inverse="_inverse_deadline", string="Deadline")

    _sql_constraints = [
        ('positive_price', 'CHECK(price >=0)', 'The Offer\'s price must be positive.')
    ]

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            computation_date = record.create_date if record.create_date else fields.date.today()
            record.date_deadline = computation_date + relativedelta(days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            computation_date = record.create_date if record.create_date else fields.date.today()
            record.validity = (record.date_deadline.date() - record.create_date.date()).days

    def accept_offer(self):
        for record in self:
            if(record.property_id.has_accepted_offer()):
                raise exceptions.UserError("Only one Offer can be accepted")
            compute_cost = record.property_id.expected_price *90/100
            if(tools.float_utils.float_compare(compute_cost, record.price, 2) > 0):
                raise exceptions.ValidationError("You can't accept an offer lower than 90% of the selling price.")
            record.status = "accepted"
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
        return True

    def decline_offer(self):
        for record in self:
            record.status = "refused"
        return True