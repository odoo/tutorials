/** @odoo-module **/

import { Component, useState, onWillStart, useEffect } from "@odoo/owl";
import { browser } from "@web/core/browser/browser";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

import { Layout } from "@web/search/layout";
import { DashboardItem } from "./dashboard_item";
import { Piechart } from "../piechart";
import { PiechartCard } from "./piechart_card";
import { NumberCard } from "./number_card";

import { useSettingsDialog } from "./dashboard_settings_hook";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";

    setup() {
      this.action = useService("action");
      this.dialogService = useService('dialog')
      this.statistics = useState(useService("awesome_dashboard.statistics"));
      this.result = useState({});
      this.hiddenItems = browser.localStorage.getItem("itemsPreference").split(',')
      this.allItems = registry.category("awesome_dashboard").getEntries().map(entries=>entries[1])
      this.items = useState(this.allItems.filter((item)=>!this.hiddenItems.includes(item.id)))
      onWillStart(async () => {
        Object.assign(this.result, await this.statistics.state.loadStatistics());
      });

      useEffect(
        () => {
          const fetch = async () => {
            Object.assign(
              this.result,
              await this.statistics.state.loadStatistics()
            );
          };
          fetch();
        },
        () => [this.statistics.state.loadStatistics]
      );
    }

    openCustomers() {
      this.action.doAction("base.action_partner_form");
    }

    openLeads() {
      this.action.doAction({
        type: "ir.actions.act_window",
        name: "Leads",
        target: "current",
        res_model: "crm.lead",
        views: [
          [false, "list"],
          [false, "form"],
        ],
      });
    }

    async openSettingsDialog() {
      const settingsDialog = await useSettingsDialog(this.dialogService)
      if (settingsDialog) {
        const hidden = browser.localStorage.getItem("itemsPreference").split(',')
        this.items.splice(0,this.items.length,...this.allItems.filter((item)=>!hidden.includes(item.id)))
      }
    }

    static components = { Layout, DashboardItem, Piechart, PiechartCard, NumberCard };
}

registry
  .category("lazy_components")
  .add("awesome_dashboard.dashboard", AwesomeDashboard);
