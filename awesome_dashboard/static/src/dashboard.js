import { Component, useState, onMounted, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";
import { PieChart } from "./pie_chart/pie_chart";
import { DashboardItem } from "./dashboarditem/dashboarditem"
import { Dialog } from "@web/core/dialog/dialog";
import { CheckBox } from "@web/core/checkbox/checkbox";
import { browser } from "@web/core/browser/browser";
import {dashboardItems} from './dashboarditems'
import { NumberCard } from "./number_card/number_card";

class AwesomeDashboard extends Component {
  static template = "awesome_dashboard.AwesomeDashboard";
  static components = { Layout, DashboardItem, PieChart,NumberCard };

  setup() {

    this.items = dashboardItems;
    this.action = useService("action");
    this.statisticsService = useService("awesome_dashboard.statistics");
    this.dialog = useService("dialog");
    this.display = {
      controlPanel: {},
    };
    this.state = useState({
      loading: true,
      disabledItems: browser.localStorage.getItem("disabledDashboardItems")?.split(",") || [],
    });

    onWillStart(async () => {
      this.statistics = await this.statisticsService.loadStatistics();
      console.log(this.statistics);
    });

    onMounted(async () => {
      await new Promise((res) => setTimeout(res, 1000));
      this.state.loading = false;
    });
  }

  openCustomers() {
    this.action.doAction("base.action_partner_form");
  }

  openLeads() {
    this.action.doAction({
      type: "ir.actions.act_window",
      name: _t("Leads"),
      target: "current",
      res_model: "crm.lead",
      views: [
        [false, "list"],
        [false, "form"],
      ],
    });
  }

  openConfiguration() {
    this.dialog.add(ConfigurationDialog, {
      items: this.items,
      disabledItems: this.state.disabledItems,
      onUpdateConfiguration: this.updateConfiguration.bind(this),
    });
  }

  updateConfiguration(newDisabledItems) {
    this.state.disabledItems = newDisabledItems;
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
        }));
    }

    done() {
        this.props.close();
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


registry
  .category("lazy_components")
  .add("AwesomeDashboard", AwesomeDashboard);
