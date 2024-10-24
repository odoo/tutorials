from odoo import api,fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type Ayve"
    _order = "name"
    _sql_constraints = [
        (
            "unique_property_type",
            "unique(name)",
            "A Property Type with the same name already exists in the Database!"
        )
    ]

    name = fields.Char(required=True)
    property_id = fields.One2many('estate.property',"property_type_id", string = "Property", )
    offer_ids = fields.One2many('estate.property.offer',"property_type_id", string = "Offer IDs")
    offer_count = fields.Integer(compute = "_compute_offer_counts", store = True)
    #sequence field is used in combination with the handle (look in property type views)
    sequence = fields.Integer('Sequence', default = 1, help = "Used to order stages. Lower is better.") 

    @api.depends("offer_ids")
    def _compute_offer_counts(self):
        for record in self:
            count=len(record.offer_ids)
            record.offer_count=count
