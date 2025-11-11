/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { Layout } from "@web/search/layout";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";
import { DashboardItem } from "./dashboard_item/dashboard_item";
import { PieChart } from "./pie_chart/pie_chart";
import { DashboardDialog } from "./dashboard_dialog/dashboard_dialog";

class AwesomeDashboard extends Component {
  static template = "awesome_dashboard.AwesomeDashboard";
  static components = { Layout, DashboardItem, PieChart, DashboardDialog };

  setup() {
    this.action = useService("action");
    this.statistics = useState(useService("awesome_dashboard.statistics"));
    this.dialog = useService("dialog");
    const removedItems = localStorage.getItem("removedItems")?.split(",") ?? [];
    this.items = useState(
      registry
        .category("awesome_dashboard")
        .getAll()
        .map((item) => ({
          ...item,
          isSelected: !removedItems.find((x) => item.id == x),
        }))
    );
  }

  openCustomersKanban() {
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
  openDashboardDialog() {
    this.dialog.add(DashboardDialog, {
      items: this.items.map((item) => ({
        id: item.id,
        description: item.description,
        isSelected: item.isSelected,
      })),
      apply: (removedIds) => {
        localStorage.setItem("removedItems", removedIds?.join(","));

        this.items.forEach((item) => {
          if (removedIds.includes(item.id)) item.isSelected = false;
          else item.isSelected = true;
        });
      },
    });
  }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
