from odoo import api, exceptions, fields, models
from datetime import timedelta

class EstatePropertyOffer(models.Model):
	_name = 'estate.property.offer'
	_description = "Property Offers"

	price = fields.Float(
		string="Offer Price")
	status = fields.Selection(
		string="Status",
		copy=False,
		selection=[
		('accepted',"Accepted"),
		('refused',"Refuesd")]
	)
	partner_id = fields.Many2one(
		'res.partner',
		string="Partner", 
		required=True)
	property_id = fields.Many2one(
		'estate.property', 
		string="Property", 
		required=True)
	validity = fields.Integer(
		string="Validity", 
		default=7)
	date_deadline = fields.Date(
		string="Date Deadline", 
		compute='_compute_date_deadline',
		inverse='_inverse_date_deadline',
		store=True)
	create_date = fields.Date(
		default=fields.Date.context_today)


	# compute date deadline from create date plus validity.
	@api.depends('create_date','validity')
	def _compute_date_deadline(self):
		for record in self:
			if record.create_date:
				record.date_deadline = record.create_date + timedelta(days=record.validity)
			else:
				record.date_deadline = False

	# inverse method to compute validity from create date and deadline
	def _inverse_date_deadline(self):
		for record in self:
			if record.create_date and record.date_deadline:
				record.validity = (record.date_deadline -
					record.create_date).days
			else:
				record.validity = 7

	# action to check if any offer accepted then shows error
	# else change state to accepted and change selling price
	def action_accept(self):
		for record in self:
			accepted_offers = record.property_id.offer_ids.filtered(
				lambda x: x.status == "accepted")

			if accepted_offers:
				raise exceptions.UserError("Only one offer can accepted.")
			record.status = 'accepted'
			record.property_id.selling_price = record.price

	# action to change offer status to refused
	def action_refuse(self):
		self.status = 'refused'
