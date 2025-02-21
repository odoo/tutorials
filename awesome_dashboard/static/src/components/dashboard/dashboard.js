import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { PieChart } from "./pie_chart/pie_chart";
import { Component, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { CheckBox } from "@web/core/checkbox/checkbox";
import { browser } from "@web/core/browser/browser";

import { DashboardItem } from "./dashboard_item/dashboard_item";

class AwesomeDashboard extends Component {
    static components = { Layout, DashboardItem, PieChart };
    static template = "awesome_dashboard.AwesomeDashboard";
    
    setup() {
        this.action = useService("action");
        this.dialog = useService("dialog");
        this.statisticsService = useService("awesome_dashboard.statistics");
        this.statistics = useState(this.statisticsService);
        this.items = registry.category("awesome_dashboard").getAll();
        this.state = useState({
            disabledItems: browser.localStorage.getItem("disabledDashboardItems")?.split(",") || []
        });
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Leads",
            res_model: "crm.lead",
            views: [[false, 'list'], [false, 'form']],
            target: "current",
        });
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
