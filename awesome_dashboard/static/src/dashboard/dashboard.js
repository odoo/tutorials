import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";
import { DashboardItem } from "./components/dashboarditem/dashboarditem";
import { Dialog } from "@web/core/dialog/dialog";
import { CheckBox } from "@web/core/checkbox/checkbox";
import { Settings } from "./components/settings/settings";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, Dialog, CheckBox };

    setup() {
        this.action = useService("action");
        this.statisticsService = useService("awesome_dashboard.statistics");
        this.statistics = useState(this.statisticsService.stats);
        this.dialog = useService("dialog");
        this.items = registry.category("awesome_dashboard").getAll();

        const storedHiddenItems = JSON.parse(localStorage.getItem('hiddenDashboardItems')) || []
        this.hiddenItems = useState(new Set(storedHiddenItems))
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: _t("Open Leads"),
            target: "current",
            res_model: "crm.lead",
            views: [[false, "list"], [false, "form"]],
        });
    }

    openSettings(){
        this.dialog.add(Settings,{
            onDone : (hiddenItems)=>{
                this.hiddenItems.clear();
                hiddenItems.forEach(id => this.hiddenItems.add(id));
            }
        });
    }

    get selectedItems(){
        return Object.values(this.items.filter(item => !this.hiddenItems.has(item.id)))
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
