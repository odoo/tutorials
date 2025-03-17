# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class ProjectTask(models.Model):
    _inherit = "project.task"

    user_ids = fields.Many2many(
        comodel_name="res.users",
        relation="project_task_user_rel",
        column1="task_id",
        column2="user_id",
        string="Assignees",
        tracking=True,
        domain=[("active", "=", True)],
    )
