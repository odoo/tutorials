from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type"
    _order = "sequence, name asc" 

    name = fields.Char(string="Name", required=True)
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")

    offer_count = fields.Integer(
        string="Offer Count",
        compute="_compute_offer_count"
    )

    sequence = fields.Integer("Sequence", default=10)
    _sql_constraints = [
        ('unique_type_name', 'UNIQUE(name)', 'The property type name must be unique.')
    ]

    def _compute_offer_count(self):
        for record in self:
            record.offer_count = self.env['estate.property.offer'].search_count([
                ('property_id.property_type_id', '=', record.id)
            ])

    def action_view_offers(self):
        return {
            'name': 'Offers',
            'type': 'ir.actions.act_window',
            'res_model': 'estate.property.offer',
            'view_mode': 'list,form',
            'domain': [('property_id.property_type_id', '=', self.id)],
            'context': {'default_property_id.property_type_id': self.id},
        }
