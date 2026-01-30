import { KanbanController } from "@web/views/kanban/kanban_controller";

import { CustomerList } from "../customer_list/customer_list";


export class AwesomeKanbanController extends KanbanController {
    static template = "awesome_kanban.AwesomeKanbanController";
    static components = { ...KanbanController.components, CustomerList };

    setup() {
        super.setup();
        this.searchKey = Symbol("isFromAwesomeKanban");
    }

    onCustomerSelected(customer_id, customer_name) {
        const customerFilters = this.env.searchModel.getSearchItems((searchItem) =>
            searchItem.isFromAwesomeKanban
        );

        for (const customerFilter of customerFilters) {
            if (customerFilter.isActive) {
                this.env.searchModel.toggleSearchItem(customerFilter.id);
            }
        }

        this.env.searchModel.createNewFilters([{
            description: customer_name,
            domain: [["partner_id", "=", customer_id]],
            isFromAwesomeKanban: true,
        }])
    }
}
