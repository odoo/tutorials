/** @odoo-module */

import { KanbanController } from "@web/views/kanban/kanban_controller";
import { CustomerList } from "./customer_list/customer_list"


export class AwesomeKanbanController extends KanbanController {
    static template = "awesome_kanban.AwesomeKanbanController";

    static components = { ...KanbanController.components, CustomerList };

    setup() {
        super.setup();
    }

    emptyFunction(customerId, customerName) {
        const customerFilters = this.env.searchModel.getSearchItems((searchItem) =>
            searchItem.isFromAwesomeKanban
        );

        for (const customerFilter of customerFilters) {
            if (customerFilter.isActive) {
                this.env.searchModel.toggleSearchItem(customerFilter.id);
            }
        }

        console.log(customerId);
        this.env.searchModel.createNewFilters([{
            description: customerName,
            domain: [["partner_id", "=", customerId]],
            isFromAwesomeKanban: true, // this is a custom key to retrieve our filters later
        }])
    };
}
