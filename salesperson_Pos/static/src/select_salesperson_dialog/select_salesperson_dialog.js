import { Component } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { Dialog } from "@web/core/dialog/dialog";

export class SelectSalespersonDialog extends Component {
  static template = "salesperson_pos.SelectSalespersonDialog";
  static props = {
    employees: Array,
    getPayload: Function,
    close: Function,
    title: String,
  };
  static components = { Dialog };

  setup() {
    this.dialog = useService("dialog");
    this.selectSalesperson = this.selectSalesperson.bind(this);
  }

  selectSalesperson(salesperson) {
    if (salesperson) {
      this.props.getPayload(salesperson);
    } else {
      this.props.getPayload(null);
    }
    this.props.close();
  }

  cancelSelection() {
    console.log("cancel triggered");
    this.props.getPayload(null);
    this.props.close();
  }
}
