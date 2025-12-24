import { Component } from "@odoo/owl";
import { Piechart } from "../pieChart/pieChart";

export class Piechartcard extends Component {
  static template = "awesome_dashboard.Piechartcard";
  static components = { Piechart };
  static props = {
    title: { type: String },
    value: { type: Object },
  };
}
