from odoo import api, fields, models


class EstatepropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'property Type'
    _order = 'sequence, name ASC'
    _sql_constraints = [
		('unique_type', 'UNIQUE (name)', 'The Type must be unique.')
	    ]

    name = fields.Char(required=True, string="Name")
    property_ids = fields.One2many('estate.property', 'property_type_id',string="Property")
    sequence = fields.Integer(string="Sequence", default=1, help="Used to order stages. Lower is better.")
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id')
    offer_count = fields.Integer(string="Offers", compute='_compute_offer_count')

    #----------------------
      #Compute Methods
    #----------------------

    @api.depends('offer_ids')
    def _compute_offer_count(self):
      for property_type in self:
        property_type.offer_count = len(property_type.property_ids.offer_ids)
