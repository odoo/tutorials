import { Component } from "@odoo/owl";
import { Counter } from "./counter";

export class Playground extends Component {
    static template = "awesome_owl.playground";

    static components = { Counter }
    static props = {};
}
