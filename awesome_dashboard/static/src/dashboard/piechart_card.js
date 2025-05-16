import { Component } from "@odoo/owl";

import { Piechart } from "../piechart";

export class PiechartCard extends Component {
    static components = { Piechart };
  
    static template = "awesome_dashboard.PiechartCard";
    static props = {
      title: String,
      data: { type: Object, shape: { m: Number, s: Number, xl: Number } },
    };
}
