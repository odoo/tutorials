from odoo import models, fields


class GFSIGrade(models.Model):
    _name = "gfsi.grade"
    _description = "GFSI Grades"

    name = fields.Char(string="Grade Name")
