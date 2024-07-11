from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _name = "estate.property.offer"
    _order = "price desc"
    _description = "Real_Estate property model"

    price = fields.Float('Price', required=True)
    status = fields.Selection(selection=[('accepted', 'Accepted'), ('refused', 'Refused')], copy=False)
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")
    property_type_id = fields.Many2one('estate.property.type', compute='_compute_property_type_id', store='True')

    @api.depends('property_id')
    def _compute_property_type_id(self):
        for record in self:
            if record.property_id and record.property_id.property_type_id:
                record.property_type_id = record.property_id.property_type_id

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.today() + relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days

    def action_accept(self):
        if self.property_id.partner_id == self.partner_id:
            raise UserError("only one offer accepted")
        self.status = "accepted"
        self.property_id.selling_price = self.price
        self.property_id.partner_id = self.partner_id

    def action_refuse(self):
        for record in self:
            if record.status == "accepted":
                record.property_id.partner_id = ""
                record.property_id.selling_price = 0.0
            record.status = "refused"

    _sql_constraints = [
        ('check_price', 'CHECK(price >= 0)',
        'The offers price should be positive')
    ]
