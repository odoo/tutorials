/** @odoo-module */
import { kanbanView } from "@web/views/kanban/kanban_view";
import { AwesomeKanbanController } from "./components/awesome_kanban_controller/awesome_kanban_controller";
import { registry } from "@web/core/registry";

export const awesomeKanbanView = {
    ...kanbanView,
    Controller: AwesomeKanbanController
};

registry.category("views").add("awesome_kanban", awesomeKanbanView);