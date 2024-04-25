/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { Dialog } from '@web/core/dialog/dialog';
import { DashboardItem } from "./dashboard_item";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, Dialog};

    setup() {
        this.dialog = useService('dialog');
        this.items = registry.category("awesome_dashboard").getAll();
        this.action = useService("action");
        this.statsService = useService("awesome_dashboard.statistics");
        this.stats_proxy = useState(this.statsService.statistics);
        this.storedConfig = JSON.parse(window.localStorage.getItem("dashboard_config"));
        if(this.storedConfig) {
            this.hidden_items = useState(this.storedConfig);
        } else {
            this.hidden_items = useState({'array': []});
        }
    }

    confirmConfiguration(arr) {
        this.hidden_items['array'] = arr;
        window.localStorage.setItem("dashboard_config", JSON.stringify(this.hidden_items));

    }

    openConfiguration() {
        this.dialog.add(ConfigDialog, {
            title: "Dashboard items configuration",
            question: "Which cards do you wish to see?",
            body: this.items,
            config: [...this.hidden_items.array],
            confirm: this.confirmConfiguration.bind(this),
        })
    }

    showCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    showLeads() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: 'Leads',
            target: 'current',
            res_model: 'crm.lead',
            views: [[false, 'tree'], [false, 'form']],
        });
    }
}
registry.category("lazy_components").add("awesome_dashboard", AwesomeDashboard);

class ConfigDialog extends Component {
    static template = "awesome_dashboard.ConfigDialog";
    static components = { Dialog };
    static props = {
        title: { type: String },
        question: { type: String },
        body: { type: Object },
        config: {type: Object},
        confirm: {type:Function},
    };

    itemCheckboxChanged(itemId, isChecked) {
        if(!isChecked) {
            if(!this.currentConfig.includes(itemId)){
                this.currentConfig.push(itemId);
             }
        } else {
            if(this.currentConfig.includes(itemId)) {
                this.currentConfig.splice(this.currentConfig.indexOf(itemId), 1);
            }
        }
    }

    setup() {
        this.currentConfig = this.props.config;
        this.itemCheckboxChanged = this.itemCheckboxChanged.bind(this);
    }

    _confirm() {
        this.props.confirm(this.currentConfig);
        this.props.close();
    }
}