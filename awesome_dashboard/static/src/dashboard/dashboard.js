import { Component, useState, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboardItem/dashboard_item";
import { Piechart } from "./pieChart/pieChart";
import { DashboardSettings } from "./dashboardSetting/dashboard_setting";
import { rpc } from "@web/core/network/rpc";

class AwesomeDashboard extends Component {
  static template = "awesome_dashboard.AwesomeDashboard";
  static components = { Layout, DashboardItem, Piechart };

  setup() {
    const dashboardItemsRegistryData = registry.category("awesome_dashboard");
    this.action = useService("action");
    this.items = dashboardItemsRegistryData.getAll();
    this.statisticServices = useService("awesome_dashboard.statistics");
    this.state = useState({ statistic: this.statisticServices.statistic });
    this.dialogService = useService("dialog");
    this.displayData = useState({
      disabledItems: [],
      isLoading: true,
    });
    onWillStart(async () => {
      try {
        // this.displayData.isLoading = true;
        const fetchedDisabledItems = await rpc(
          "/web/dataset/call_kw/res.users/get_dashboard_settings",
          {
            model: "res.users",
            method: "get_dashboard_settings",
            args: [],
            kwargs: {},
          }
        );
        this.displayData.disabledItems = fetchedDisabledItems;
      } catch (error) {
        console.error(
          "Error loading initial dashboard settings from server:",
          error
        );
        this.displayData.disabledItems = [];
      } finally {
        this.displayData.isLoading = false;
      }
    });
  }
  openCustomers() {
    this.action.doAction("base.action_partner_form");
  }

  async openLeads(activity) {
    this.action.doAction({
      type: "ir.actions.act_window",
      name: "Journal Entry",
      target: "current",
      res_id: activity.res_id,
      res_model: "crm.lead",
      views: [
        [false, "list"],
        [false, "form"],
      ],
    });
  }

  updateConfiguration(newUncheckedItems) {
    this.displayData.disabledItems.length = 0;
    this.displayData.disabledItems.push(...newUncheckedItems);
  }

  openSetting() {
    this.dialogService.add(DashboardSettings, {
      items: this.items,
      initialUncheckedItems: this.state.uncheckedItems,
      updateConfiguration: this.updateConfiguration.bind(this),
    });
  }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
