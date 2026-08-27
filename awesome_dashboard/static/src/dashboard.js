import {Component, onWillStart, useState, onWillUnmount } from "@odoo/owl";
import {_t} from "@web/core/l10n/translation";
import {useService} from "@web/core/utils/hooks";
import {Layout} from "@web/search/layout";
import {registry} from "@web/core/registry";
import {DashboardItem} from "./dashboard_item/dashboard_item"
import {PieChart} from "./chart/pie_chart/pie_chart"

class AwesomeDashboard extends Component {
     static template = "awesome_dashboard.AwesomeDashboard";
     static components = { Layout, DashboardItem, PieChart };

     setup() {
         this.display = {
             controlPanel: {},
         };
         this.action = useService("action");

         this.dashStatsService = useService("awesome_dashboard.statistics");

         this.state = useState({
             stats: {},
         });

         onWillStart(async () => {
             this.state.stats = await this.dashStatsService.loadStatistics();
         })

         const intervalId = setInterval(async () => {
             const newStats = await this.dashStatsService.loadStatistics();
             // Update the stats state keeping the reference
             Object.assign(this.state.stats, newStats);
             }, 1000*60*10);

         onWillUnmount(() => {
             clearInterval(intervalId);
         });
     }

    openCustomers() {
         this.action.doAction("base.action_partner_form", {
             viewType: "kanban"
         });
    }

    openLeads() {
         this.action.doAction({
             type: 'ir.actions.act_window',
             name: _t('Leads'),
             target: 'new',
             res_model: "crm.lead",
             views: [
                 [false, "list"],
                 [false, "form"]
             ],
         });
    }
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
