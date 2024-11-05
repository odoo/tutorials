/** @odoo-module */

import {Component, onWillStart, useState} from "@odoo/owl";
import {useService} from "@web/core/utils/hooks";
import {KeepLast} from "@web/core/utils/concurrency";
import {fuzzyLookup} from "@web/core/utils/search";
import {Pager} from "@web/core/pager/pager";


export class CustomerList extends Component {
    static template = "awesome_kanban.CustomerList";
    static props = {
        selectCustomer: Function,
    }
    static components = { Pager };

    get displayedPartners() {
        return this.filterOnName(this.state.searchName)
    }

    setup() {
        this.orm = useService('orm');
        this.partners = useState({data: []});
        this.state = useState({
            searchName: "",
            displayActive: false,
        })
        this.keepLast = new KeepLast();
        this.pager = useState({offset: 0, limit: 15});

        onWillStart(async () => {
            const {records, length} = await this.loadCustomer();
            this.partners.data = records;
            this.pager.total = length;
        });
    }

    loadCustomer() {
        const {offset, limit} = this.pager;
        const domain = this.state.displayActive ? [["has_active_order", "=", true]] : [];
        return this.orm.webSearchRead("res.partner", domain, {
            specification: { display_name: {} },
            limit: limit,
            offset: offset,
        });
    }

    filterOnName(name) {
        if (name) {
            return fuzzyLookup(name, this.partners.data, (partner) => partner.display_name)
        } else {
            return this.partners.data;
        }
    }

    async onCheckbox(ev) {
        this.state.displayActive = ev.target.checked;
        this.pager.offset = 0;
        const {records, length} = await this.keepLast.add(this.loadCustomer());
        this.partners.data = records;
        this.pager.total = length;
    }

    onSearchInput(ev) {
        this.searchName = ev.target.value;
        this.filterOnName(this.searchName);
    }

    async onUpdatePager(newState) {
        Object.assign(this.pager, newState);
        const {records} = await this.loadCustomer();
        this.partners.data = records;
        this.filterOnName(this.filterName);
    }

}
