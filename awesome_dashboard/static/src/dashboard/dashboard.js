import { Component, useState, onWillStart } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { DashboardItem } from "./components/dashboard_item/dashboard_item";
import { NumberCard } from "./components/number_card/number_card";
import { PieChart } from "./components/pie_chart/pie_chart";
import { SettingDialog } from "./setting/setting_dialog";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, NumberCard, PieChart };

    setup() {
        this.dialogService = useService("dialog");
        this.action = useService("action");
        this.statisticsService = useService("awesome_dashboard.statistics");
        this.statistics = useState(this.statisticsService.data);
        this.state = useState({ hiddenItems: JSON.parse(localStorage.getItem("awesome_dashboard_hidden_items")) || [] });
    }

    openCustomers = () => {
        this.action.doAction("base.action_partner_customer_form", {
            views: [[false, "kanban"]],
        });
    }

    openLeads = () => {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Leads",
            res_model: "crm.lead",
            views: [
                [false, "list"],
                [false, "form"]
            ]
        });
    }

    getFilteredItems = () => {
        const hiddenSet = new Set(this.state.hiddenItems);
        return registry.category("awesome_dashboard.items").getAll().filter(item => !hiddenSet.has(item.id));
    }

    openSettings = () => {
        this.dialogService.add(SettingDialog, {
            onApply: (hiddenItems) => {
                localStorage.setItem("awesome_dashboard_hidden_items", JSON.stringify(hiddenItems));
                this.state.hiddenItems = hiddenItems;
            }
        });
    }
}

registry.category("lazy_components").add("awesome_dashboard.dashboard", AwesomeDashboard);