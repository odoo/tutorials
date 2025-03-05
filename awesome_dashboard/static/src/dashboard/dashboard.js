import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./components/dashboard_item/dashboard_item"
import { PieChart } from "./components/pie_chart/pie_chart";
import { ConfigurationDialog } from "./components/configuration_dialog/configuration_dialog";
import { browser } from "@web/core/browser/browser";


class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, PieChart };

    setup() {
        this.action = useService("action");
        this.result = useState(useService("awesome_dashboard.statistics"));
        this.items = registry.category("awesome_dashboard").getAll();
        this.dialog = useService("dialog");
        this.state = useState({
            disabledItems: browser.localStorage.getItem("disabledDashboardItems")?.split(",") || [],
        });
    }

    onClickCustomers(){
        this.action.doAction("base.action_partner_form")
    }


    onClickLeads(){
        this.action.doAction({
            "type": "ir.actions.act_window",
            "name": "All Leads",
            "res_model": "crm.lead",
            "views": [[false, "list"],[false, "form"]]
        })
    }

    openDashboardConfiguration() {
        this.dialog.add(ConfigurationDialog, {
        items: this.items,
        disabledItems: this.state.disabledItems,
        onUpdateConfiguration: this.updateDashboardConfiguration.bind(this),
        });
    }

    updateDashboardConfiguration(newDisabledItems) {
        this.state.disabledItems = newDisabledItems;
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);