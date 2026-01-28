import { Component, onWillStart, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { fuzzyLookup } from "@web/core/utils/search";
import { Pager } from "@web/core/pager/pager";

export class CustomerList extends Component {
    static template = "awesome_kanban.CustomerList"

    static props = {
        selectCustomer: { type: Function, optional: true }
    }

    static components = {
        Pager
    }

    setup() {
        this.orm = useService("orm");
        this.customers = [];
        this.filters = useState({ active: false, search: "" })
        this.page = useState({ current: 0, limit: 5 })

        onWillStart(async () => {
            const data = await this.orm.webSearchRead("res.partner", [], {
                specification: {
                    name: {},
                    id: {},
                    opportunity_ids: {}
                },
            });

            this.customers = data.records;
        })
    }

    getFilteredCustomers() {
        let result = this.customers.filter(c => {
            return !this.filters.active || c.opportunity_ids.length > 0
        })

        if(this.filters.search.length > 0) {
            result = fuzzyLookup(this.filters.search, result, (c) => c.name)
        }

        return result;
    }

    getCustomersOfPage(customers) {
        if(this.page.current > customers.length) {
            this.page.current = Math.floor(customers.length / this.page.limit) * this.page.limit;
        }

        return customers.slice(this.page.current, this.page.current + this.page.limit);
    }

    updatePage(ev){
        this.page.current = ev.offset;
    }
}
