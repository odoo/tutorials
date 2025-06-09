import { Component } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";

export class DBModal extends Component {
  static template = "awesome_dashboard.db_modal";
  static components = { Dialog };

  static props = ['items','chart']

  setup() {
    this.items = this.props.items;
    this.chart = this.props.chart;
    this.visibleList = this.items.reduce((acc, crr) => {
      if (crr?.isVisible) {
        acc?.push(crr?.id);
      }
      return acc;
    }, []);

    if (this.chart.isVisible) {
      this.visibleList.push("chart");
    }
  }

  handleItemToggle = (_, id) => {
    if (this.visibleList.includes(id)) {
      this.visibleList = this.visibleList.filter((i) => i !== id);
    } else {
      this.visibleList.push(id);
    }
  };

  handleApplySetting() {
    this.items.forEach((item) => {
      item.isVisible = this.visibleList.includes(item?.id);
    });

    this.chart.isVisible = this.visibleList.includes("chart");

    localStorage.setItem(
      "dashboardItemVisibility",
      JSON.stringify(this.visibleList)
    );
    this.props.close();
  }
}
