from odoo import api, models, fields
from datetime import timedelta, date
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
  _name = 'estate.property.offer'
  _description = 'this is estate property offer Database model created by meem (meet moradiya)...'

  price = fields.Float('Price')
  status = fields.Selection(
    string='Status',
    copy='False',
    selection=[
      ('accepted', 'Accepted'),
      ('refused', 'Refused')
    ]
  )
  partner_id = fields.Many2one('res.partner', 'Partner', required=True)
  property_id = fields.Many2one('estate.property', 'Property ID', required=True)
  validity = fields.Integer('Validity (days)', default=7)
  date_deadline = fields.Date('Deadline', compute='_compute_deadline', inverse='_inverse_deadline')





  ########## Compute Methods ##########

  @api.depends('validity', 'date_deadline')
  def _compute_deadline(self):
    for record in self:
      record.date_deadline = date.today() + timedelta(days = record.validity)

  def _inverse_deadline(self):
    for record in self:
      record.validity = max((record.date_deadline - date.today()).days, 0)



  ########## Normal Methods ##########

  def action_accepted(self):
    for record in self:
      accepted_offer = record.property_id.offer_ids.filtered(lambda offer: offer.status == 'accepted')
      if accepted_offer:
        first_accepted_offer = accepted_offer[0]
        raise UserError(f"An offer with {first_accepted_offer.partner_id.name} at a price of {first_accepted_offer.price} has already been accepted.")

      record.status = 'accepted'
      record.property_id.buyer = record.partner_id
      record.property_id.selling_price = record.price

  def action_refused(self):
    for record in self:
      if record.status == 'accepted':
        record.property_id.selling_price = 0
        record.property_id.buyer = False

      record.status = 'refused'


########## constraints ##########

  _sql_constraints = [
        ('check_offer_price', 'CHECK(price > 0)',
         'The Expected price must be Positive.')
    ]  
  