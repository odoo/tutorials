import { KanbanController } from "@web/views/kanban/kanban_controller";
import { registry } from "@web/core/registry";
import { kanbanView } from "@web/views/kanban/kanban_view"
import { CustomerList } from "./customer_list/customer_list";

class AwesomeKanbanController extends KanbanController {
    static template = "awesome_kanban.AwesomeKanbanController";

    static components = {
        CustomerList,
        ...KanbanController.components
    }

    selectCustomer(customer) {
        const customerFilters = this.env.searchModel.getSearchItems((searchItem) =>
            searchItem.isFromAwesomeKanban
        );

        let exists = false;

        for (const customerFilter of customerFilters) {
            let toggleCondition;

            if(customerFilter.description === customer.name) {
                exists = true;
                toggleCondition = !customerFilter.isActive;
            }
            else toggleCondition = customerFilter.isActive;

            if (toggleCondition) {
                this.env.searchModel.toggleSearchItem(customerFilter.id);
            }
        }

        if(!exists) {
            this.env.searchModel.createNewFilters([{
                description: customer.name,
                domain: [["partner_id", "=", customer.id]],
                isFromAwesomeKanban: true,
            }]);
        }
    }
}

const awesomeKanbanView = {
    ...kanbanView,
    Controller: AwesomeKanbanController
}

registry.category("views").add("awesome_kanban", awesomeKanbanView);
