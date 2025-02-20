import { Component , useState, markup } from "@odoo/owl";
import {Counter} from  './counter/counter';
import {Card} from './card';
import {TodoList} from './todo/todo_list'
export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components={Card,Counter,TodoList};
    setup(){
        this.title1='Card 1';
        this.title2="Card 2";
        this.content1="<div class='text-primary'>some text</div>";
        this.content2=markup("<div class='text-primary'>some text</div>");
        this.state=useState({sum:0});
    }
    onChange(){
        this.state.sum+=1
        console.log(this.state.sum);
    }
}
