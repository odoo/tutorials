import {_t } from "@web/core/l10n/translation";
import { Component, onWillStart, useState} from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./DashboardItem/DashboardItem";
import { PieChart } from "./PieChart/PieChart";
import { SettingsDialog } from "./SettingsDialog/SettingsDialog";
import { browser } from "@web/core/browser/browser";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout , DashboardItem, PieChart};

    setup()
    {
        this.action = useService("action");
        this.result = useState(useService("awesome_dashboard.statistics"));
        this.items = registry.category("awesome_dashboard").getAll();
        this.dialog = useService("dialog");
        this.state = useState({disabledItems : browser.localStorage.getItem("disabledDashboardItems")?.split(",")||[]});
        this.Customer = _t("Customer");
        this.Leads = _t("Leads");

    }
    openCustomers()
    {
        this.action.doAction("base.action_partner_form")
    }
    openLeads()
    {
        this.action.doAction(({
            type: 'ir.actions.act_window',
            name: "All leads",
            res_model: 'account.move',
            views: [[0,'list'],[1,'form']]
        }));
    }
    openSettings()
    {
        this.dialog.add(SettingsDialog, {
            disabled:this.state.disabledItems,
            items:this.items,
            OnChange:this.updateSettings.bind(this),
        })
    }
    updateSettings(disabledItems)
    {
        this.state.disabledItems = disabledItems;
    }
}


registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);

