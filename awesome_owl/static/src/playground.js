import { Component, useState, markup} from "@odoo/owl";
import { Counter } from "./counter";
import { Card } from "./card";
import { TodoList } from "@awesome_owl/todo/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter,Card,TodoList};

    
    setup(){
        const stitle1 = markup("<strong>Title1</strong>");
        const scontent1 = markup("<i><u>nice <a href='https://youtu.be/Aq5WXmQQooo?si=JiVfEeuosJhEFoC9'>text!</a></u></i>");
        
        this.incrementSum = this.incrementSum.bind(this);

        this.state = useState({
            title1: stitle1,
            content1: scontent1,
            sum:0,
        });
    }
    incrementSum(){
        this.state.sum++;
    }

    

}
