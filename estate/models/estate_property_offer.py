from odoo import api, fields, models
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Properties Offers defined"

    # order
    _order = "price desc"

    price = fields.Float(string="Price")
    status = fields.Selection(string="Status", selection=[('accepted', 'Accepted'), ('refused', 'Refused')], copy=False)
    partner_id = fields.Many2one("res.partner", string="Partner Id", required=True)
    property_id = fields.Many2one("estate.property", string="Property Id", required=True, ondelete='cascade')
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_deadline", inverse="_inverse_deadline", store=True)

    # sql constraints
    _sql_constraints = [('offer_price_positive', 'CHECK(price > 0)', "The offer Price cannot be negative")]

    # stat button
    property_type_id = fields.Many2one("estate.property.type", related="property_id.property_type_id", store=True)

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            record.date_deadline = datetime.now() + timedelta(days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            if record.date_deadline:
                record.validity = relativedelta(record.date_deadline, datetime.now()).days
            else:
                record.validity = 0

    def action_accept_offer(self):
        if self.property_id.buyer:
            raise UserError("Only one offer can be accepted")
        self.status = 'accepted'
        self.property_id.buyer = self.partner_id
        self.property_id.selling_price = self.price
        self.property_id.state = 'offer accepted'
        return True

    def action_refuse_offer(self):
        if self.property_id.buyer == self.partner_id:
            self.property_id.buyer = ''
            self.property_id.selling_price = 0.00
        self.status = 'refused'
        return True

    def unlink(self):
        for offer in self:
            if offer.status == 'accepted':
                offer.property_id.buyer = ''
                offer.property_id.selling_price = 0.00
        return super().unlink()

    @api.model
    def create(self, vals):
        props = self.env["estate.property"].browse(vals["property_id"])
        if props.offer_ids:
            max_val = max(props.mapped("offer_ids.price"))
            if float_compare(vals["price"], max_val, precision_rounding=0.01) <= 0:
                raise UserError("The offer must be higher than %.2f" % max_val)
        props.state = 'offer received'
        return super().create(vals)
