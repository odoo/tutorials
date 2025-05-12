from odoo import fields, models


class EstatePropertyType(models.Model):

    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    _order = "sequence, name"
    _sql_constraints = [
        ("check_name", "UNIQUE(name)", "The name must be unique"),
    ]

    name = fields.Char("Name", required=True)
    sequence = fields.Integer("Sequence", default=10)

    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")

    offer_count = fields.Integer(string="Offers Count", compute="_compute_offer")
    offer_ids = fields.Many2many("estate.property.offer", string="Offers", compute="_compute_offer")

    def _compute_offer(self):
            #         # data = [
            #     {
            #         'property_type_id': (5, "Villa"), 
            #         'property_type_id_count': 3,
            #         'ids': [101, 102, 103]
            #     }
            # ]
        # Imagine self.env is like Google Search for Odoo models.(self.env) doesn't contain the result.It gives you access to what you searched for
        data = self.env["estate.property.offer"].read_group(
            [("property_id.state", "!=", "canceled"), ("property_type_id", "!=", False)], # filter records
            ["ids:array_agg(id)", "property_type_id"], # do aggregation on grouped records and what field to return 
            # apply array_agg(put all in array) on ids -> alias ids & property_type_id -> to know what id and group it belongs to
            ["property_type_id"],#group by property_type_id
        )
        # mapped_count = {5: 3, 10: 5} making them easy to use
        mapped_count = {d["property_type_id"][0]: d["property_type_id_count"] for d in data}
        mapped_ids = {d["property_type_id"][0]: d["ids"] for d in data}
        for prop_type in self:
            # If the ID exists in mapped_count, use its value (e.g., 3).If not, default to 0.
            prop_type.offer_count = mapped_count.get(prop_type.id, 0)
            prop_type.offer_ids = mapped_ids.get(prop_type.id, [])
            # Note : we are directly assinging value here and not using write method because we are in compute method and dont want to write in db
            

    def action_view_offers(self):
        res = self.env.ref("estate.estate_property_offer_action").read()[0]
        res["domain"] = [("id", "in", self.offer_ids.ids)]
        return res
