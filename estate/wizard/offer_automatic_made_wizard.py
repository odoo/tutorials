from odoo import api, fields, models
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


class AutomaticOfferWizard(models.TransientModel):
    _name = 'estate.offer.automatic.wizard'
    _description = 'Create New Offers for multiple properties'

    price = fields.Float(string="Price")
    status = fields.Selection(
        string="Status",
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused')
        ], copy=False)
    buyer_id = fields.Many2one("res.partner", string="Partner Id", required=True)

    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_deadline", inverse="_inverse_deadline", store=True)

    # sql constraints
    _sql_constraints = [('offer_price_positive', 'CHECK(price > 0)', "The offer Price cannot be negative")]

    # stat button

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

    def action_add_offer(self):
        properties = self.env['estate.property'].browse(self.env.context.get('active_ids', []))
        for props in properties:
            self.env['estate.property.offer'].create({
                'price': self.price,
                'partner_id': self.buyer_id.id,
                'property_id': props.id,
                'date_deadline': self.date_deadline
            })
        return {'type': 'ir.actions.act_window_close'}
