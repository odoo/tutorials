# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api
from dateutil.relativedelta import relativedelta


class Animal(models.Model):
    _name = "awesome_shelter.animal"
    _description = "Animal"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(required=True)
    picture = fields.Image("Picture")
    type_id = fields.Many2one("awesome_shelter.animal_type", "Type", required=True)
    pictogram = fields.Image(related="type_id.pictogram")
    state = fields.Selection(
        selection=[
            ("on_site", "On site"),
            ("adopted", "Adopted"),
        ],
        default="on_site",
        required=True,
        string="State",
        tracking=True,
    )
    race_id = fields.Many2one("awesome_shelter.animal_race", "Race")
    notes = fields.Html("Notes")
    dropper_id = fields.Many2one("res.partner", "Dropper")
    drop_date = fields.Date("Drop date", default=fields.Date.today(), required=True)
    owner_id = fields.Many2one("res.partner", "Owner", tracking=True)
    birth_date = fields.Date("Birth date")

    is_present_for_six_month = fields.Boolean(
        compute="_compute_is_present_for_six_month"
    )

    @api.depends("drop_date")
    def _compute_is_present_for_six_month(self):
        for record in self:
            record.is_present_for_six_month = (
                fields.Date.today() + relativedelta(months=-6) < record.drop_date
            )
