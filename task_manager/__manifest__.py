{
    "name": "Task Manager",
    "application": True,
    "installable": True,
    "author": "sngoh",
    "depends": ["mail"],
    "license": "LGPL-3",
    "data": [
        "security/ir.access.csv",
        "data/ir_cron_data.xml",
        "views/task_manager_tags_view.xml",
        "views/task_manager_view.xml",
        "views/task_manager_menus.xml",
    ],
}
