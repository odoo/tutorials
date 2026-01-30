import { Component, onWillStart, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { fuzzyLookup } from "@web/core/utils/search";


export class CustomerList extends Component {
    static template = "awesome_kanban.CustomerList";

    static props = { selectCustomer: Function };

    setup() {
        super.setup();
        this.orm = useService("orm");
        this.customers = useState({ data: [] });
        this.state = useState({ nameFilter: "", isActiveChecked: false });

        onWillStart(async () => this.customers.data = await this.loadCustomers())
    }

    get displayedCustomers() {
        return this.filterCustomersByName(this.state.nameFilter);
    }

    async toggleActiveCustomerFilter(ev) {
        this.state.isActiveChecked = ev.target.checked;
        this.customers.data = await this.loadCustomers();
    }

    loadCustomers() {
        let domain = this.state.isActiveChecked ? [["opportunity_ids", "!=", false]] : [];
        return this.orm.searchRead("res.partner", domain, ["display_name"]);
    }

    filterCustomersByName(filter) {
        return filter === "" ? this.customers.data : fuzzyLookup(filter, this.customers.data, (customer) => customer.display_name);
    }
}
