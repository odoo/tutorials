/** @odoo-module **/

import { Component, onWillStart, useState, useEffect } from "@odoo/owl";
import { _t } from "@web/core/l10n/translation";
import { browser } from "@web/core/browser/browser";
import { CheckBox } from "@web/core/checkbox/checkbox";
import { Dialog } from "@web/core/dialog/dialog";
import { useService } from "@web/core/utils/hooks";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { DashboardItem } from "./dashboard_item";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem }
    setup() {
        this.action = useService("action");
        this.dialog = useService("dialog");
        this.statisticsService = useService('awesome_dashboard.statistics');
        this.items = registry.category("awesome_dashboard.items").getAll() || [];
        this.state = useState({
            disabledItems: browser.localStorage.getItem("disabledDashboardItems")?.split(",") || []
        });
        this.result = useState(this.statisticsService.data)
        this.chartData = useState({ labels: [], data: [] });
        this.chartData = {
            labels: [],
            data: []
        };
        useEffect(() => {
            this.chartData.labels = Object.keys(this.result.orders_by_size);
            this.chartData.data = Object.values(this.result.orders_by_size);
            console.log("Updated chartData", this.chartData);
        });
        onWillStart(async () => {
            try {
                this.chartData.labels = Object.keys(this.result.orders_by_size);
                this.chartData.data = Object.values(this.result.orders_by_size);
            } catch (error) {
                console.error("Failed to fetch statistics:", error);
            }
        });
    }

    customersKanbanView() {
        this.action.doAction("base.action_partner_form")
    }

    openConfiguration() {
        this.dialog.add(ConfigurationDialog, {
            items: this.items,
            disabledItems: this.state.disabledItems,
            onUpdateConfiguration: this.updateConfiguration.bind(this),
        })
    }

    updateConfiguration(newDisabledItems) {
        this.state.disabledItems = newDisabledItems;
    }

    open_leads() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: _t('Leads'),
            target: 'current',
            res_model: 'crm.lead',
            views: [[false, 'list'], [false, 'form']]
        })
    }
}

class ConfigurationDialog extends Component {
    static template = "awesome_dashboard.ConfigurationDialog";
    static components = { Dialog, CheckBox };
    static props = ["close", "items", "disabledItems", "onUpdateConfiguration"];

    setup() {
        this.items = useState(this.props.items.map((item) => {
            return {
                ...item,
                enabled: !this.props.disabledItems.includes(item.id),
            }
        }));
    }

    done() {
        this.props.close();
    }

    onChange(checked, changedItem) {
        changedItem.enabled = checked;
        const newDisabledItems = Object.values(this.items).filter(
            (item) => !item.enabled
        ).map((item) => item.id)

        browser.localStorage.setItem(
            "disabledDashboardItems",
            newDisabledItems,
        );

        this.props.onUpdateConfiguration(newDisabledItems);
    }

}

registry.category("lazy_components").add("awesome_dashboard.dashboard", AwesomeDashboard);
