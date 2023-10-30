/** @odoo-module */

import { useService } from "@web/core/utils/hooks";
import { Component, onWillStart, useState} from "@odoo/owl";
import { KeepLast } from "@web/core/utils/concurrency";
import { fuzzyLookup } from "@web/core/utils/search";

export class CustomerList extends Component {
    static template = "awesome_kanban.CustomerList";
    static props = {
        selectCustomer: {
            type: Function,
        },
    };

    setup() {
        this.orm = useService("orm");
        this.partners = useState({ data: [] });
        this.keepLast = new KeepLast();
        this.state = useState({
            searchString: "",
            displayActiveCustomers: false,
        })

        onWillStart(async () => {
            this.partners.data = await this.loadCustomers();
        })
    }

    get displayedPartners() {
        return this.filterCustomers(this.state.searchString);
    }

    async onChangeActiveCustomers(ev) {
        this.state.displayActiveCustomers = ev.target.checked;
        this.partners.data = await this.keepLast.add(this.loadCustomers());
    }

    filterCustomers(name) {
        if (name) {
            return fuzzyLookup(name, this.partners.data, (partner) => partner.display_name);
        } else {
            return this.partners.data;
        }
    }

    loadCustomers() {
        const domain = this.state.displayActiveCustomers ? [["opportunity_ids", "!=", false]] : [];
        return this.orm.searchRead("res.partner", domain, ["display_name"]);
    }

}
