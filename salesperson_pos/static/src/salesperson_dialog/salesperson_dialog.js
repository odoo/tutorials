import { Component, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
export class SalespersonListPopup extends Component {
  static template = "salesperson_pos.SalespersonListPopup";
  static props = {
    title: String,
    salespersonList: Array,
    confirm: Function,
    close: Function,
  };

  static components = { Dialog };
  setup() {
    this.selectSalesperson = this.selectSalesperson.bind(this);
  }

  selectSalesperson(salesperson) {
    this.props.confirm(salesperson);
    this.props.close();
  }

  cancelSelection() {
    this.props.confirm(null);
    this.props.close();
  }
}
