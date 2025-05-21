import { Component } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { Dropdown } from "@web/core/dropdown/dropdown";

export class SalesPersonLine extends Component {
  static template = "pos_salesperson.SalesLine";
  static components = { Dropdown };
  static props = [
    "close",
    "salesperson",
    "isSelected",
    "onClickUnselect",
    "onClickSalesPerson",
  ];

  setup() {
    this.ui = useService("ui");
  }
}
