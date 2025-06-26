/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from '@web/search/layout';
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item";
import { items } from "./dashboard_items";
import { NumberCard } from "./number_card";
import { PieChartCard } from "./pie_chart_card";
import { Dialog } from "@web/core/dialog/dialog";
import { CheckBox } from "@web/core/checkbox/checkbox";
import { browser } from "@web/core/browser/browser";



class AwesomeDashboard extends Component {
    static components = {DashboardItem, NumberCard, PieChartCard, Layout}
    static template = "awesome_dashboard.AwesomeDashboard";

    setup() {
        this.state = useState({
            disabledItems: browser.localStorage.getItem("disabledDashboardItems")?.split(",") || []
        });
        this.action = useService("action");
        this.statisticsService = useService("awesome_dashboard.statistics");
        this.dialog = useService("dialog");
        this.statistics = useState(this.statisticsService.statistics);
        this.items = registry.category("awesome_dashboard").getAll();
    }

    openConfiguration() {
        this.dialog.add(ConfigurationDialog, {
            items: this.items,
            disabledItems: this.state.disabledItems,
            onUpdateConfiguration: this.updateConfiguration.bind(this),
        })
    }

    updateConfiguration(disabledItems) {
        this.state.disabledItems = disabledItems;
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Leads",
            res_model: "crm.lead",
            views: [[false, "list"], [false, "form"]],
            target: "current",
        });
    }
}


class ConfigurationDialog extends Component {
    static components = { Dialog, CheckBox };
    static template = "awesome_dashboard.ConfigurationDialog";
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
