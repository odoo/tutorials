from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError
import logging
from odoo.tools import float_compare

_logger = logging.getLogger(__name__)

class EstatePropertyOffer(models.Model):
    _name = 'estate_property_offer'
    _description = "Estate property offer"
    _order = "price desc"

    price=fields.Float(default=0)
    state = fields.Selection([
      ('accepted', 'Accepted'),
      ('refused', 'Refused'),
      ],
      copy=False, string="Status")
    partner_id=fields.Many2one('res.partner', string="Partner", required=True)
    property_id=fields.Many2one('estate.property', required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")
    property_type_id =  fields.Many2one(related='property_id.property_type_id', store=True)

    _check_price_strictly_positive = models.Constraint(
        'CHECK(price > 0)',
        'The offer price should be strictly positive.',
    )

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            start_date = record.create_date.date() if record.create_date else fields.Date.today()
            record.date_deadline = start_date + relativedelta(days =+ record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            start_date = record.create_date.date() if record.create_date else fields.Date.today()
            record.validity = (record.date_deadline - start_date).days

    def action_confirm(self):
        for record in self:
            if 'accepted' in record.property_id.offer_ids.mapped('state'):
                raise UserError("An offer has already been accepted for that property.")
            else:
                self.write({'state': 'accepted'})
                return record.property_id.write(
                  {
                      "state": "offer_accepted",
                      "selling_price": record.price,
                      "buyer_id": record.partner_id,
                      "salesperson_id": self.env.user
                  }
                )

    def action_refuse(self):
        for record in self:
            if record.state == 'accepted':
                record.property_id.selling_price = 0
                record.property_id.buyer_id = None
                record.property_id.salesperson_id = None
            return self.write({'state': 'refused'})

    @api.model
    def create(self, vals_list):
        _logger.warning("CREATE")
        for vals in vals_list:
            # Do some business logic, modify vals...
            _logger.warning("RECORD PRICE : %s", vals['price'])

            if vals.get("property_id") and vals.get("price"):
                offer_property = self.env['estate.property'].browse(vals['property_id'])

                if offer_property.offer_ids:
                  max_offer = max(offer_property.offer_ids.mapped('price'))
                  _logger.warning("MAX offers PRICE : %s", max_offer)
                  if float_compare(vals["price"], max_offer, precision_rounding=0.01) <= 0:
                      raise UserError("The offer must be higher than %.2f" % max_offer)

                offer_property.state = 'offer_received'

        # Then call super to execute the parent method
        return super().create(vals_list)
