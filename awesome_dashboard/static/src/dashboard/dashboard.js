/** @odoo-module **/
import { Component, useState, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { Dialog } from "@web/core/dialog/dialog";
import { CheckBox } from "@web/core/checkbox/checkbox";
import { browser } from "@web/core/browser/browser";
import { PieChart } from "./pie_chart/pie_chart"
// import { rpc } from "@web/core/network/rpc"
// import { items } from "./dashboard_item";


class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, PieChart };

    setup() {
        this.myService = useService("awesome_dashboard_service");
        this.action = useService("action");
        this.statistics = useService("awesome_dashboard.statistics");
        this.dialogService = useService("dialog");
        // this.items = items;
        this.items = registry.category("awesome_dashboard.items").getAll();


        // stats for statistics cards
        this.stats = useState(this.statistics);

        // Local Storage Data
        const savedDisabled =
            browser.localStorage
                .getItem("disabledDashboardItems")
                ?.split(",") || [];

        this.ui = useState({
            disabledItems: savedDisabled,
        });

        //rpc calls every time means reopeing dashboard refreshes value
        // onWillStart(async () => {
        //     this.stats.stats = await rpc("/awesome_dashboard/statistics", {})
        // });

        //memoize means reopeing dashboard will not refreshes, value will store in cache
        // onWillStart(async () => {
        //     this.stats.stats = await this.statistics.loadStatistics();
        // });

    }

    inc() {
        this.myService.inc();
        this.render(); // simple way to refresh UI for now
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            res_model: "crm.lead",
            views: [
                [false, "list"],
                [false, "form"]
            ],
        });
    }
    openConfiguration() {
        this.dialogService.add(ConfigurationDialog, {
            items: this.items,
            disabledItems: this.ui.disabledItems,
            onUpdateConfiguration: this.updateConfiguration.bind(this),
        });
    }

    updateConfiguration(newDisabledItems) {
        this.ui.disabledItems = newDisabledItems;
    }

    openOrdersBySize(size) {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Orders",
            res_model: "sale.order",
            views: [[false, "list"], [false, "form"]],
            domain: [["order_line.product_id.product_template_attribute_value_ids.name", "=", size.toUpperCase()]],
        });
    }

}

class ConfigurationDialog extends Component {
    static template = "awesome_dashboard.ConfigurationDialog";
    static components = { Dialog, CheckBox };
    static props = ["close", "items", "disabledItems", "onUpdateConfiguration"];

    setup() {
        this.items = useState(
            this.props.items.map((item) => ({
                ...item,
                enabled: !this.props.disabledItems.includes(item.id),
            }))
        );
    }

    done() {
        this.props.close();
    }

    onChange(checked, changedItem) {
        changedItem.enabled = checked;

        const newDisabledItems = this.items
            .filter((item) => !item.enabled)
            .map((item) => item.id);

        browser.localStorage.setItem(
            "disabledDashboardItems",
            newDisabledItems
        );

        this.props.onUpdateConfiguration(newDisabledItems);
    }
}


// registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);

