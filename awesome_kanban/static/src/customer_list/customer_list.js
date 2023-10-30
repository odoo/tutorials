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
        this.displayedPartners = useState({ data: [] });
        this.filterName = "";
        this.keepLast = new KeepLast();

        onWillStart(async () => {
            this.partners.data = await this.loadCustomers([]);
            this.displayedPartners.data = this.partners.data;
        })
    }

    async onChangeActiveCustomers(ev) {
        const checked = ev.target.checked;
        const domain = checked ?  [["opportunity_ids", "!=", false]] : [];
        this.partners.data = await this.keepLast.add(this.loadCustomers(domain));
        this.filterCustomers(this.filterName);
    }

    onCustomerFilter(ev) {
        this.filterName = ev.target.value;
        this.filterCustomers(ev.target.value);
    }

    filterCustomers(name) {
        if (name) {
            this.displayedPartners.data = fuzzyLookup(
                name,
                this.partners.data,
                (partner) => partner.display_name
            );
        } else {
            this.displayedPartners.data = this.partners.data;
        }
    }

    loadCustomers(domain) {
        return this.orm.searchRead("res.partner", domain, ["display_name"]);
    }

}
