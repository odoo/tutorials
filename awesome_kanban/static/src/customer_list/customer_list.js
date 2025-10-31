/** @odoo-module */

import { Component, onWillStart, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { KeepLast } from "@web/core/utils/concurrency";
import { fuzzyLookup } from "@web/core/utils/search";
import { Pager } from "@web/core/pager/pager";

export class CustomerList extends Component {
    static template = "awesome_kanban.CustomerList";

    static components = { Pager };

    static props = {
        selectCustomer: Function
    }

    setup() {
        this.orm = useService("orm");
        this.customers = useState({ data: [] });
        this.keepLast = new KeepLast();
        this.state = useState({ displayActiveCustomers: false, searchString: ''})
        onWillStart(async () => {
            this.customers.data = await this.loadCustomers([]);
            this.pager.total = this.customers.data.length;
        })
        this.pager = useState({ offset: 0, limit: 20 });
    }

    loadCustomers() {
        const domain = this.state.displayActiveCustomers ? [["opportunity_ids", "!=", false]] : [];
        return this.orm.searchRead("res.partner", domain, ["display_name"]);
    }

    get displayedCustomers() {
        const displayCustomers = this.filterCustomers(this.state.searchString);
        this.pager.total = displayCustomers.length;
        return displayCustomers.slice(this.pager.offset, this.pager.offset + this.pager.limit);
    }

    async checkboxChange(ev) {
        this.pager.offset = 0;
        this.state.displayActiveCustomers = ev.target.checked;
        this.customers.data = await this.keepLast.add(this.loadCustomers());
        this.pager.total = this.customers.data.length;
    }

    filterCustomers(name) {
        if (name) {
            const filteredCustomers = fuzzyLookup(
                name,
                this.customers.data,
                (customer) => customer.display_name
            );
            if(this.pager.offset > filteredCustomers.length) this.pager.offset = 0;
            return filteredCustomers;
        } else {
            return this.customers.data;
        }
    }

    onUpdatePager(data) {
        Object.assign(this.pager, data);
    }
    
}
