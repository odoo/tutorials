from odoo import fields, models, api

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type like House, Apartment, Penthouse"
    _order = "name"

    #---------------------------------------------------------------------
    # Fields
    #---------------------------------------------------------------------
    name = fields.Char(required=True)
    sequence = fields.Integer(string="Seqeuence", default=1)

    #---------------------------------------------------------------------
    # Relations
    #---------------------------------------------------------------------
    property_ids = fields.One2many("estate.property", "property_type_id", string="Property Id")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id", string="Type Id")
    offer_count = fields.Integer()

    #---------------------------------------------------------------------
    # Compute Methods
    #---------------------------------------------------------------------
    @api.depends("offer_ids")
    def _compute_offer_count(self):
        counter = 0
        for record in self:
            counter +=1
        self.offer_count =  counter

