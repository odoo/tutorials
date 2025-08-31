import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { CogMenu } from "@web/search/cog_menu/cog_menu";
import { useService } from "@web/core/utils/hooks";
import { browser } from "@web/core/browser/browser";
import { DashboardItem } from "./dashboard_item";
import { PieChart } from "./pie_chart/pie_chart";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, CogMenu, DashboardItem, PieChart };

    setup() {
        this.action = useService("action");
        this.statisticStateService = useService("statistics_service");
        this.items =  registry.category("awesome_dashboard_items").getAll();
        this.result = useState(this.statisticStateService.loadStatisticsRealTime());
        
        this.state = useState({
            openPopup: false, 
            hiddenItems: this.getHiddenItemsFromLocalStorage(),
        });
        this.disableItem = this.disableItem.bind(this);

        /// Other methods of retrieving data: rpc call every time & memoize rpc call
        // onWillStart(async () => {
            // this.result = await this.statisticStateService.loadStatisticsRPC();
            // this.result = await this.statisticStateService.loadStatistics();
        // });
    }

    openCustomersKanban() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: 'Leads',
            target: 'current',
            res_model: 'crm.lead',
            views: [
                [false, "list"],
                [false, "form"],
            ],
        });
    }

    getHiddenItemsFromLocalStorage() {
        return JSON.parse(browser.localStorage.getItem("dashboard.hiddenItems")) || [];
    }

    setHiddenItemsToLocalStorage(hiddenItems) {
        browser.localStorage.setItem("dashboard.hiddenItems", JSON.stringify(hiddenItems));
    }

    openConfiguration() {
        this.hiddenItems = this.getHiddenItemsFromLocalStorage();
        this.state.openPopup = true;
    }
    
    closeConfiguration() {
        this.state.openPopup = false;
    }

    disableItem(id) {        
        const index = this.hiddenItems.indexOf(id);
        if (index !== -1){
            this.hiddenItems.splice(index, 1);
        } else {
            this.hiddenItems.push(id);
        }
    }

    applyChanges() {
        this.state.hiddenItems = this.hiddenItems;
        this.setHiddenItemsToLocalStorage(this.hiddenItems)
        this.closeConfiguration();
    }

}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
