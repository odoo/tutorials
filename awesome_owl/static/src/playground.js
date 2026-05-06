import { Component } from "@odoo/owl";
import { Counter } from "./components/counter/counter";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter };
}
