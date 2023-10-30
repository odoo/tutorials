import { useService } from "@web/core/utils/hooks";
import { Component, onWillStart, useState} from "@odoo/owl";
import { KeepLast } from "@web/core/utils/concurrency";
import { fuzzyLookup } from "@web/core/utils/search";
import { Pager } from "@web/core/pager/pager";

export class CustomerList extends Component {
    static components = { Pager };
    static template = "awesome_kanban.CustomerList";
    static props = {
        selectCustomer: {
            type: Function,
        },
    };

    setup() {
        this.orm = useService("orm");
        this.partners = useState({ data: [] });
        this.pager = useState({ offset: 0, limit: 20 });
        this.keepLast = new KeepLast();
        this.state = useState({
            searchString: "",
            displayActiveCustomers: false,
        })

        onWillStart(async () => {
            const { length, records } = await this.loadCustomers();
            this.partners.data = records;
            this.pager.total = length;
        })
    }

    get displayedPartners() {
        return this.filterCustomers(this.state.searchString);
    }

    async onChangeActiveCustomers(ev) {
        this.state.displayActiveCustomers = ev.target.checked;
        this.partners.data = await this.keepLast.add(this.loadCustomers());
        this.pager.offset = 0;
        const { length, records } = await this.keepLast.add(this.loadCustomers());
        this.partners.data = records;
        this.pager.total = length;
    }

    filterCustomers(name) {
        if (name) {
            return fuzzyLookup(name, this.partners.data, (partner) => partner.display_name);
        } else {
            return this.partners.data;
        }
    }

    loadCustomers() {
        const { limit, offset } = this.pager;
        const domain = this.state.displayActiveCustomers ? [["opportunity_ids", "!=", false]] : [];
        return this.orm.webSearchRead("res.partner", domain, {
            specification: {
                "display_name": {},
            },
            limit,
            offset,
        })
    }


    async onUpdatePager(newState) {
        Object.assign(this.pager, newState);
        const { records } = await this.loadCustomers();
        this.partners.data = records;
        this.filterCustomers(this.filterName);
    }
}
