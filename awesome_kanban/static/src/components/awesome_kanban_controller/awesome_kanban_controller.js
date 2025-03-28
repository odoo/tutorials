import { KanbanController } from "@web/views/kanban/kanban_controller";
import { CustomerList } from "../customer_list/customer_list";

export class AwesomeKanbanController extends KanbanController {
    static template = "awesome_kanban.awesomeKanbanController";
    static components = { ...KanbanController.components, CustomerList }
    setup() {
        super.setup();
    }
    selectCustomer(customer_name, customer_id) {
        const customerFilters = this.env.searchModel.getSearchItems((searchItem) => searchItem.isFromAwesomeKanban);
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