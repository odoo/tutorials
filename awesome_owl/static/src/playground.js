/** @odoo-module **/

import { Component, useState, xml } from "@odoo/owl";
import { Counter } from "./counter/counter"


export class Playground extends Component {
  static template = "awesome_owl.playground";
  static components = { Counter };
}
