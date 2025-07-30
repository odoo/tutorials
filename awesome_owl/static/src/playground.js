/** @odoo-module **/

import { markup, Component, useState} from "@odoo/owl";
import { Counter } from './counter/counter';
import { Card } from './card/card';
import { TodoList } from './todolist/todolist';

export class Playground extends Component {

    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList }

    setup(){
        this.state = useState({ sum: 0 });
    }

    incrementSum()
    {
       this.state.sum++
    }

}
