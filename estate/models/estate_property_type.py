from odoo import fields, models, api


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "ESTATE Property Type"
    _order = "sequence, name"

    name = fields.Char('Name', required=True)
    description = fields.Text(string="Description")
    sequence = fields.Integer('Sequence', default=10)
    offer_count = fields.Integer('Offers Count', compute="_compute_total_offers")  # Computed Field

    property_ids = fields.One2many(  # One2Many (List of Properties with a Type)
        comodel_name="estate.property",
        inverse_name="type_id",
        string="Properties",
    )

    offer_ids = fields.One2many(  # One2Many (List of Offers with a Type)
        comodel_name="estate.property.offer",
        inverse_name="property_type_id",
        string="Offers",
    )

    @api.depends("offer_ids")
    def _compute_total_offers(self):
        for property_type in self:
            property_type.offer_count = len(property_type.property_ids.mapped("offer_ids"))

    # SQL constraints
    _unique_name = models.Constraint(
        'UNIQUE(name)',
        'A property property type name must be unique',
    )

    def action_view_offers(self):
        return {
            "type": "ir.actions.act_window",
            "res_model": "estate.property.offer",
            "name": "Offers",
            "view_mode": "list",
            "domain": [("property_id.type_id", "=", self.id)],
            "context": {"default_property_id": False},
        }
