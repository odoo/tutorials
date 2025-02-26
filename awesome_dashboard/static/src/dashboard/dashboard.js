/** @odoo-module **/

import { Component, useState, useRef, onMounted } from "@odoo/owl";

import { _t } from "@web/core/l10n/translation";
import { Dialog } from "@web/core/dialog/dialog";
import { useService } from "@web/core/utils/hooks";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";

import { DashboardItem } from "./dashboard_item"
import { PieChart } from "./pie_chart"

export class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Dialog, Layout, DashboardItem, PieChart }

    setup() {
        this.action = useService("action");
        this.statisticsLoader = useService("awesome_dashboard.statistics");

        this.statistics = useState(this.statisticsLoader);

        this.items = registry.category("awesome_dashboard").getAll();
        this.enabledCards = useState({});
        this.items.forEach((item) => {
            this.enabledCards[item.id] = true;
        });

        this.dialogService = useService("dialog");
        // useSubEnv({dialogData: {}})
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: _t('Leads'),
            res_model: 'account.move',
            views: [[false, 'list'], [false, 'form']]
        });
    }

    openDialog() {
        const dialogProps = {
            items: this.items,
            enabledItems: this.enabledCards,
            doneCallback: (values) => {
                Object.assign(this.enabledCards, values);
            }
        };
        this.dialogService.add(ConfigurationDialog, dialogProps);
    }
}

class ConfigurationDialog extends Component {
    static template = "awesome_dashboard.configuration_dialog"
    static components = { Dialog };
    static props = {
        items: {
            type: Array,
            element: Object,
        },
        enabledItems: Object,
        doneCallback: Function,
        close: Function
    }

    setup() {
        this.refs = new Map();
        this.props.items.forEach(item => {
            let ref = useRef(item.id)
            this.refs.set(item.id, ref);
            if (this.props.enabledItems[item.id]) {
                onMounted(() => ref.el.checked = true);
            }
        });
    }

    onDone() {
        let values = {};
        this.refs.entries().forEach(([id, ref]) => {
            values[id] = ref.el.checked;
        });
        this.props.doneCallback(values);
        this.props.close();
    }
}

registry.category("lazy_components").add("awesome_dashboard.dashboard", AwesomeDashboard);
