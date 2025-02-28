import { Component, onWillStart, useState } from '@odoo/owl';
import { KeepLast } from '@web/core/utils/concurrency';
import { useService } from '@web/core/utils/hooks';
import { fuzzyLookup } from '@web/core/utils/search';
import { Pager } from '@web/core/pager/pager';

export class CustomerList extends Component {
    static template = 'awesome_kanban.CustomerList';
    static props = {
        selectCustomer: Function
    };
    static components = { Pager };

    setup() {
        this.pager = useState({
            limit: 20,
            total: 0,
            offset: 0
        });

        this.keepLast = new KeepLast();
        this.orm = useService('orm');
        this.state = useState({
            customers: [],
            filteredCustomers: [],
            activeFilter: false,
            searchPattern: '',
        });
        onWillStart(async () => {
            await this.load();
        });
    }

    async load() {
        const domain = [];
        if (this.state.activeFilter) {
            domain.push(['opportunity_ids', '!=', false]);
        }
        const specification = {
            ['name']: {},
            ['display_name']: {},
            ['opportunity_ids']: {},
        };
        const { length, records } = await this.keepLast.add(this.orm.webSearchRead('res.partner', domain, {
            specification,
            offset: this.pager.offset,
            limit: this.pager.limit,
        }));
        this.pager.total = length;
        this.state.customers = records;
        this._updateFiltered();
    }

    _updateFiltered() {
        if (this.state.searchPattern) {
            this.state.filteredCustomers = fuzzyLookup(this.state.searchPattern, this.state.customers, record => record.display_name);
        } else {
            this.state.filteredCustomers = this.state.customers;
        }
    }

    search() {
        this._updateFiltered();
    }

    async toggleActiveFilter() {
        await this.load();
    }

    displayedCustomers() {
        return this.state.filteredCustomers;
    }

    async changePage({ offset, limit }) {
        this.pager.offset = offset;
        this.pager.limit = limit;
        await this.load();
    }
};
