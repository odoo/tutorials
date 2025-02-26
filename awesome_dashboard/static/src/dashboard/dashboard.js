import { Component,useState, onWillStart } from "@odoo/owl";
import { DashboardItem } from "./DashboardItem/dashboardItem";
import { Layout } from "@web/search/layout"
import { Dialog } from "@web/core/dialog/dialog";
import { PieChart } from "./PieChartCard/PieChart";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { browser } from "@web/core/browser/browser";
import { CheckBox } from "@web/core/checkbox/checkbox";


class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = {Layout , DashboardItem,PieChart}
    setup(){
    this.action= useService('action')
    this.statisticsService = useService("awesome_dashboard.statistics");
    this.stats={}
    onWillStart(async()=>{
       this.stats= await this.statisticsService.loadStatistics();
    });
    
    this.items=registry.category("awesome_dashboard").getAll();
    this.dialog = useService("dialog");
    this.dialog_state = useState({
        disabledItems: browser.localStorage.getItem("disabledDashboardItems")?.split(",") || []
    });
    }

    openCustomers(){
        this.action.doAction('base.action_partner_form')
    }
    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: ("Leads"),
            res_model: "crm.lead",
            target: "current",
            views: [[false,'list'],[false,'form']]
        });
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
registry.category("lazy_components").add("awesome_dashboard.AwesomeDashboard", AwesomeDashboard);
