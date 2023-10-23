/** @odoo-module  */

import { KanbanController } from "@web/views/kanban/kanban_controller";
import { CustomerList } from "./customer_list/customer_list";

export class AwesomeKanbanController extends KanbanController {
    static components = { ...KanbanController.components, CustomerList}
    static template = "awesome_kanban.AwesomeKanbanController";

    setup() {
        super.setup();
    }

    selectCustomer(customer_id) {
        console.log(customer_id);
    }
}
