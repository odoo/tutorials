import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item";
import { PieChart } from "./pie_chart";
import { dashboardItems } from "./dashboard_items";
import { Dialog } from "@web/core/dialog/dialog";
import { CheckBox } from "@web/core/checkbox/checkbox";
import { browser } from "@web/core/browser/browser";


class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem , PieChart };

    setup() {
        this.action = useService("action");
        this.statisticsService = useService("statistics");
        this.stats = useState(this.statisticsService.stats);
        this.items= registry.category("awesome_dashboard").getAll();
        this.dialog = useService("dialog");
        this.dialog_state = useState({
            disabledItems: browser.localStorage.getItem("disabledDashboardItems")?.split(",") || []
        });

        /*onWillStart(async () => {
            this.stats = await this.statisticsService.loadStatistics();
            console.log(this.stats);
        });*/
    }

    openConfiguration() {
        this.dialog.add(ConfigurationDialog, {
            items: this.items,
            disabledItems: this.dialog_state.disabledItems,
            onUpdateConfiguration: this.updateConfiguration.bind(this),
        })
    }

    updateConfiguration(newDisabledItems) {
        this.dialog_state.disabledItems = newDisabledItems;
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
            views: [[false, "list"], [false, "form"]],
        });
    }


}

/* const myService = {
    dependencies: ["notification"],
    start(env, { notification }) {
        let counter = 1;
        setInterval(() => {
            notification.add(`Tick Tock ${counter++}`);
        }, 1000);
    },
};



registry.category("services").add("myService", myService); */

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
        }))
    }

    onDone() {
        this.props.close()
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
registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
