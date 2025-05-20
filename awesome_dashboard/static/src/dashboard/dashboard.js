  /** @odoo-module **/
  import { useService } from "@web/core/utils/hooks";
  import { Component, onWillStart, useState, useEffect } from "@odoo/owl";
  import { rpc } from "@web/core/network/rpc";
  import { registry } from "@web/core/registry";
  import { Layout } from "@web/search/layout";
  import { DashboardItem } from "./dashboardItem";
  import { PieChart } from "./pie/pie";
import { AwesomeDashboardSettingsDialog } from "./dashboard_dilaog";
import { _t } from "@web/core/l10n/translation";

  class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    
    setup() {
      const removedItems = JSON.parse(localStorage.getItem("awesome_dashboard_hidden_items")) || [];
      this.statisticsService = useService("awesome_dashboard.statistics");
      this.state = useState({
        res: this.statisticsService.data,
        items:registry.category("awesome_dashboard").getEntries(),
        hiddenItems: new Set(removedItems), 
        isSettingsOpen: false,
        translatableString: _t("This is Translatable String")
      });
      // console.log(this.state.hiddenItems);
      
      this.action = useService("action");
      this.display = {
        controlPanel: {},
      };
      onWillStart(async () => {
        await this.loadSettings();  // Now it runs at the correct time
        
    });
    }
    static components = {
      Layout,
      DashboardItem,
      PieChart,
      AwesomeDashboardSettingsDialog
    };
    openCustomersView() {
      this.action.doAction("base.action_partner_form");
    }
    toggleSettings() {
    this.state.isSettingsOpen = !this.state.isSettingsOpen;
  }
  
  async loadSettings() {
    const res = await rpc('/awesome_dashboard/getItems',{});
    this.state.hiddenItems = new Set(JSON.parse(res.hiddenItems));
  }

  async saveDashboardSettings() {
    await rpc('/awesome_dashboard/setItems', {
        hiddenItems: JSON.stringify([...this.state.hiddenItems]),
    });
  }

  openSettingsDialog() {
    this.env.services.dialog.add(AwesomeDashboardSettingsDialog, {
        items: this.state.items,
        hiddenItems: [...this.state.hiddenItems], // Convert Set to array
        onApply: (updatedHiddenItems) => {
          if (!this.state.hiddenItems) {
            this.state.hiddenItems = new Set();  
          }
        
          this.state.hiddenItems = new Set(updatedHiddenItems); 
          localStorage.setItem("awesome_dashboard_hidden_items", JSON.stringify([...this.state.hiddenItems]));
          this.state.isSettingsOpen = false;
          this.saveDashboardSettings()
          this.env.services.dialog.closeAll();

        },
    });
}    
    async openLeadsView() {
      this.action.doAction({
        name: "Leads",
        type: "ir.actions.act_window",
        res_model: "crm.lead",
        view_mode: "list,form",
        views: [
          [false, "list"],
          [false, "form"],
        ],
        target: "current", 
      });
    }
  }
  registry
    .category("lazy_components")
    .add("AwesomeDashboard", AwesomeDashboard);
