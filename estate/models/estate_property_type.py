from odoo import  fields,models,api

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property type is defined"

    _order = "name asc"

    name = fields.Char(required=True)
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")

    property_ids = fields.One2many('estate.property','property_type_id')
    offer_ids = fields.One2many('estate.property.offer','property_type_id',string='offers')

    _sql_constraints = [
        ('property_type_unique','unique(name)','property type should be unique')
    ]

    offer_count = fields.Integer(string="Offer Count", compute="_compute_offer_count")

    @api.depends('property_ids.offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = sum(len(property.offer_ids) for property in record.property_ids)


