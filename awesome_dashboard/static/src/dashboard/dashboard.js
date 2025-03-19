/** @odoo-module **/

import { Component, onWillStart, reactive, useState, onMounted } from '@odoo/owl';
import { registry } from '@web/core/registry';
import { Dialog } from '@web/core/dialog/dialog';
import { Layout } from '@web/search/layout';
import { useService } from '@web/core/utils/hooks';
import { DashboardItem } from './dashboard_item';
import { rpc } from '@web/core/network/rpc';
import { browser } from "@web/core/browser/browser";

class AwesomeDialog extends Component {
    static template = 'awesome_dashboard.Dialog';
    static components = { Dialog };

    async setup() {
        this.items = registry.category('awesome_dashboard').getAll();
        this.dataFetcher = useService('awesome_dashboard.data');
        this.data = useState(this.dataFetcher.getData());
        this.invisible = useState([]);
        onWillStart(async () => {
            await this.dataFetcher.loadStatistics();
        });
        onMounted(() => {
            this.dataFetcher.loadInvisible();
            this.invisible.push(...this.data.invisible);
        });
    }

    toggle(event) {
        // use array instead of set because not many items
        const input = event.target;
        const index = this.invisible.findIndex(element => element == input.dataset.id);
        if (index == -1) {
            input.checked = false;
            this.invisible.push(input.dataset.id);
        } else {
            input.checked = true;
            this.invisible.splice(index, 1);
        }
    }

    apply() {
        this.dataFetcher.updateInvisible(this.invisible);
        this.props.close();
    }
}

class AwesomeDashboard extends Component {
    static template = 'awesome_dashboard.AwesomeDashboard';
    static components = { Layout, DashboardItem, AwesomeDialog };

    openDialog() {
        this.dialog.add(AwesomeDialog);
    }

    async setup() {
        this.items = registry.category('awesome_dashboard').getAll();
        this.action = useService('action');
        this.dialog = useService('dialog');
        const dataFetcher = useService('awesome_dashboard.data');
        this.data = useState(dataFetcher.getData());
        onWillStart(async () => {
            await dataFetcher.loadStatistics();
        });

        onMounted(() => {
            dataFetcher.loadInvisible();
        });
    }

    showCustomers() {
        this.action.doAction('base.action_partner_customer_form');
    }

    openLeads() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: 'Leads',
            res_model: 'crm.lead',
            views: [[false, 'list'], [false, 'form']],
        });
    }
}

const dataService = {
    start() {
        const data = reactive({
            stats: null,
            invisible: []
        });
        return {
            getData() {
                return data;
            },
            async loadStatistics() {
                if (!data.stats) {
                    data.stats = await rpc('/awesome_dashboard/statistics');
                    setInterval(async () => {
                        data.stats = await rpc('/awesome_dashboard/statistics');
                    }, 10000 * 60);
                }
            },
            loadInvisible() {
                const invisible = browser.localStorage.getItem('invisible');
                if (invisible) {
                    data.invisible = JSON.parse(invisible);
                }
            },
            updateInvisible(invisible) {
                data.invisible = invisible;
                browser.localStorage.setItem('invisible', JSON.stringify(invisible));
            }
        }
    }
};

registry.category('services').add('awesome_dashboard.data', dataService);
registry.category('lazy_components').add('awesome_dashboard.dashboard', AwesomeDashboard);
