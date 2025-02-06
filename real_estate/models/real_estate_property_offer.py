from odoo import fields, models

class PropertyOffer(models.Model):
	_name = 'real.estate.property.offer'
	_description = "Real Estate Property Offers Table"

	price = fields.Float("Offer Price")
	status = fields.Selection(
		string="Status",
		copy=False,
		selection=[
		('accepted',"Accepted"),
		('refused',"Refuesd")]
	)
	partner_id = fields.Many2one('res.partner',string="Partner", required=True)
	property_id = fields.Many2one('real.estate.property', string="Property", required=True)
