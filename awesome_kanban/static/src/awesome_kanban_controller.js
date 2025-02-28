import { KanbanController } from '@web/views/kanban/kanban_controller';
import { CustomerList } from './customer_list';

export class AwesomeKanbanController extends KanbanController {
    static template = 'awesome_kanban.AwesomeKanbanController';
    static components = { ...KanbanController.components, CustomerList };

    selectCustomer(customer) {
        const customerFilters = this.env.searchModel.getSearchItems((searchItem) =>
            searchItem.isFromAwesomeKanban
        );
        
        for (const customerFilter of customerFilters) {
            if (customerFilter.isActive) {
                this.env.searchModel.toggleSearchItem(customerFilter.id);
            }
        }

        this.env.searchModel.createNewFilters([{
            description: customer.display_name,
            domain: [['partner_id', '=', customer.id]],
            isFromAwesomeKanban: true,
        }]);
    }
};
