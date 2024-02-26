/** @odoo-module */

import { Component, reactive, useState } from "@odoo/owl";

export class DashboardItem extends Component {
  static template = "awesome_dashboard.dashboardItem";
  static props = {
    slots: {
      type: Object,
      shape: {
        default: Object,
      },
    },
    size: {
      type: Number,
      default: 1,
      optional: true,
    },
  };
  setup() {
    this.ui = useState(this.createUI());
  }

  debounce(func, wait, immediate) {
    let timeout;
    return function () {
      const context = this;
      const args = arguments;
      function later() {
        timeout = null;
        if (!immediate) {
          func.apply(context, args);
        }
      }
      const callNow = immediate && !timeout;
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
      if (callNow) {
        func.apply(context, args);
      }
    };
  }

  createUI() {
    const getIsMobile = () => window.innerWidth <= 768;

    const ui = reactive({ isMobile: getIsMobile() });

    const updateEnv = this.debounce(() => {
      const isMobile = getIsMobile();
      if (ui.isMobile !== isMobile) {
        ui.isMobile = isMobile;
      }
    });
    window.addEventListener("resize", updateEnv);
    return ui;
  }
}
