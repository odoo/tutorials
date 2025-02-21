/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { Counter } from "./component/counter/counter";
import { Card } from "./component/card/card";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card };
}
