/** @odoo-module **/
import {Component, useState} from "@odoo/owl";
import {TodoList} from "./todo_list";


export class Todoo extends Component {
    static template = "oxp.Todoo";
    static components = {TodoList};
    static props = {};
    static nID = 2;

    setup() {
        this.elements = useState([
            {id: 1, name: "Default List"},
        ]);
    }

    addTodoList(){
        const id = Todoo.nID++;
        this.elements.push({id: id, name:`List ${id}`});
    }

    removeList(id){
        this.elements.splice(this.elements.findIndex(list => list.id === id), 1);
    }


}
