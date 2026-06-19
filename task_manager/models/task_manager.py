from odoo import api, Command, fields, models
from odoo.exceptions import UserError


class TaskManagerTask(models.Model):
    _name = "task.manager"
    _inherit = ["mail.thread"]
    _description = "Task Manager"

    name = fields.Char(tracking=True, required=True)
    active = fields.Boolean(default=True)
    assigned_user = fields.Many2one("res.users", tracking=True)
    deadline = fields.Datetime(tracking=True, required=True)
    status = fields.Selection(
        string="Status",
        selection=[
            ("new", "New"),
            ("in_progress", "In Progress"),
            ("done", "Done"),
        ],
        default="new",
        tracking=True,
    )
    tag_ids = fields.Many2many("task.manager.tags")
    days_remaining = fields.Integer(compute="_compute_days_remaining")
    count_of_assignes = fields.Integer(compute="_compute_count_of_assignes")

    @api.depends("deadline")
    def _compute_days_remaining(self):
        for task_manager in self:
            task_manager.days_remaining = (
                task_manager.deadline - fields.Datetime.today()
            ).days

    @api.depends("assigned_user")
    def _compute_count_of_assignes(self):
        for task_manager in self:
            task_manager.count_of_assignes = len(task_manager.assigned_user)

    @api.onchange("assigned_user")
    def _onchange_assigned_user(self):
        tag_name = "assigned"

        for task_manager in self:
            if not task_manager.assigned_user:
                assigned_tag = task_manager.env["task.manager.tags"].search(
                    [("name", "=", tag_name)],
                )
                if assigned_tag:
                    task_manager.tag_ids = [Command.unlink(assigned_tag.id)]
                continue
            if task_manager.tag_ids.filtered(lambda t: t.name == tag_name):
                continue
            assigned_tag = task_manager.env["task.manager.tags"].search(
                [("name", "=", tag_name)]
            )
            if not assigned_tag:
                assigned_tag = task_manager.env["task.manager.tags"].create(
                    {"name": tag_name}
                )
            task_manager.tag_ids = [Command.link(assigned_tag.id)]

    def write(self, vals):
        is_archiving = "active" in vals
        for task_manager in self:
            if task_manager.status == "done" and not is_archiving:
                raise UserError("Cannot update task's details in the Done state.")

        return super().write(vals)

    def quick_archive(self):
        if self:
            tasks = self.filtered(lambda t: t.status == "done" and t.active)
        else:
            tasks = self.env["task.manager"].search(
                [("status", "=", "done"), ("active", "=", True)]
            )
        if tasks:
            tasks.action_archive()

    def print_task_count(self):
        task_count = self.env["task.manager"].search_count([("active", "=", True)])
        return {
            "effect": {
                "fadeout": "slow",
                "message": f"{task_count} Tasks are there.",
                "img_url": "/web/static/img/smile.svg",
                "type": "rainbow_man",
            }
        }

    def generate_multiple_tasks(self):
        tasks = [
            {"name": "Generated Task 1", "deadline": fields.Datetime.today()},
            {"name": "Generated Task 2", "deadline": fields.Datetime.today()},
        ]
        self.env["task.manager"].create(tasks)

    def _auto_archive(self):
        done_tasks = self.env["task.manager"].search(
            [("status", "=", "done"), ("active", "=", True)],
        )
        done_tasks.action_archive()
