import { Component, onWillStart, useState, useRef } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { fuzzyLookup } from "@web/core/utils/search";
import { Pager } from "@web/core/pager/pager";

export class CustomerList extends Component {
    static props = ["selectCustomer"];
    static template = "awesome_kanban.customerListView";
    static components = { Pager };

    setup() {
        this.orm = useService("orm");
        this.state = useState({ only_active: false, search: "", pager: { offset: 0, total: 0 }, change: false});
        this.limit = 20;

        onWillStart(async () => {
            this.data = await this.orm.searchRead("res.partner", [], ["display_name", "opportunity_ids"]);
            this.active_customers = this.data.filter(item => item.opportunity_ids.length > 0);
            this.state.pager.total = this.data.length;
        });
    }

    _change() {
        this.state.change = true;
    }

    _changePager({ offset }) {
        this.state.pager.offset = offset;
    }

    _getCurrentCustomersSet() {
        let data = this.state.only_active ? this.active_customers : this.data;
        let search_result = this.state.search !== "" ? fuzzyLookup(this.state.search, data, (d) => d.display_name) : data;
        if (this.state.change) {
            this.state.pager.offset = 0;
            this.state.pager.total = search_result.length;
            this.state.change = false;
        }
        return search_result.slice(this.state.pager.offset, this.state.pager.offset + this.limit);
    }
}