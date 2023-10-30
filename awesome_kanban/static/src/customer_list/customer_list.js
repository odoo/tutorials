import { useService } from "@web/core/utils/hooks";
import { Component, onWillStart, useState} from "@odoo/owl";
import { KeepLast } from "@web/core/utils/concurrency";

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

        onWillStart(async () => {
            this.partners.data = await this.loadCustomers([]);
        })
    }

    async onChangeActiveCustomers(ev) {
        const checked = ev.target.checked;
        const domain = checked ?  [["opportunity_ids", "!=", false]] : [];
        this.partners.data = await this.keepLast.add(this.loadCustomers(domain));
    }

    loadCustomers(domain) {
        return this.orm.searchRead("res.partner", domain, ["display_name"]);
    }

}
