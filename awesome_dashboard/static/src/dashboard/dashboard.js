import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { rpc } from "@web/core/network/rpc";
import { Layout } from "@web/search/layout";
import { CheckBox } from "@web/core/checkbox/checkbox";
import { Dialog } from "@web/core/dialog/dialog";

import { DashboardItem } from "./dashboard_item/dashboard_item";
import { PieChart } from "./pie_chart/pie_chart";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, PieChart };

    setup() {
        this.action = useService("action");
        this.statisticsService = useService("statistics");
        this.stats = {};
        onWillStart(async () => {
            const data = await this.statisticsService.loadStatistics();
            Object.assign(this.stats, data); 
        });


        this.items = registry.category("awesome_dashboard.items").getAll();

        // onWillStart(async () => {
        //     this.stats = await rpc("/awesome_dashboard/statistics");
        // })

        // Fetch statistics only when the component is first mounted
        /*  onWillStart(async () => {
                 this.stats = await this.statisticsService.loadStatistics();
                 // console.log(this.stats);
                 
             }); */

        this.dialog = useService("dialog");
        this.remove_items = useState({
            removedItems:
                window.localStorage
                    .getItem("awesome_dashboard_removed_items")
                    ?.split(",") || [],
        });
    }


    updateConfiguration(newRemovedItems) {
        this.remove_items.removedItems = newRemovedItems;
    }

    openConfiguration() {
        this.dialog.add(ConfigurationDialog, {
            items: this.items,
            removedItems: this.remove_items.removedItems,
            onUpdateConfiguration: this.updateConfiguration.bind(this),
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
            target: "current",
            views: [
                [false, "list"],
                [false, "form"],
            ],
        });
    }
}

class ConfigurationDialog extends Component {
    static template = "awesome_dashboard.ConfigurationDialog";
    static components = { Dialog, CheckBox };
    static props = ["close", "items", "removedItems", "onUpdateConfiguration"];

    setup() {
        this.items = useState(
            this.props.items.map((item) => ({
                ...item,
                enabled: !this.props.removedItems.includes(item.id),
            }))
        );
    }

    onDone() {
        this.props.close();
    }

    onChange(checked, changedItem) {
        changedItem.enabled = checked;
        const newRemovedItems = this.items
            .filter((item) => !item.enabled)
            .map((item) => item.id);
        window.localStorage.setItem(
            "awesome_dashboard_removed_items",
            newRemovedItems
        );

        this.props.onUpdateConfiguration(newRemovedItems);
    }
}

registry
    .category("lazy_components")
    .add("awesome_dashboard.dashboard", AwesomeDashboard);
registry
    .category("actions")
    .add("awesome_dashboard.dashboard", AwesomeDashboard);
