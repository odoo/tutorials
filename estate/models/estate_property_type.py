from odoo import models, api, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "sequence,name"

    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "property_type_id")
    sequence = fields.Integer("Sequence", default=1)
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer(compute="_compute_offer_count")

    _check_type_name = models.Constraint(
        "UNIQUE(name)", "Property type should be unique."
    )

    @api.depends('property_ids.offer_ids')
    def _compute_offer_count(self):
        Offer = self.env['estate.property.offer']

        data = Offer.read_group(
            domain=[('property_id', 'in', self.property_ids.ids)],
            fields=['property_id'],
            groupby=['property_id'],
        )

        count_dict = {
            group['property_id'][0]: group['property_id_count']
            for group in data
        }

        for record in self:
            record.offer_count = sum(
                count_dict.get(prop.id, 0) for prop in record.property_ids
            )
