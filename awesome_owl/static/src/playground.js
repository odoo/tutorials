/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import {Counter} from "./counter";
import {Card} from "./card";
import {Todolist} from "./todo/todo_list";

export class Playground extends Component {
    static components = {Counter, Card, Todolist};
    static template = "awesome_owl.playground";
}
