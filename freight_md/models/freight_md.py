from odoo import api, fields, models


class FreightMD(models.Model):
    _name = "freight.md"
    _description = "Freight MD"

    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code")
    country_id = fields.Many2one(
        "res.country",
        string="Country",
        required=True,
        ondelete="restrict",
        options={"no_create": True, "no_open": True},
    )
    display_name = fields.Char(
        string="Display Name", compute="_compute_display_name", store=True
    )
    is_air = fields.Boolean(string='Air')
    is_sea = fields.Boolean(string='Sea')
    is_inland = fields.Boolean(string='Inland')

    status = fields.Boolean(string="Active", default=True)

    @api.depends("name", "country_id")
    def _compute_display_name(self):
        for record in self:
            if record.name and record.country_id:
                record.display_name = f"{record.name} - {record.country_id.name}"
            else:
                record.display_name = ""
