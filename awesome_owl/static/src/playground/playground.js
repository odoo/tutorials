import { Component, useState } from '@odoo/owl';
import { Counter } from '../counter/counter';
import { Card } from '../card/card';

export class Playground extends Component {
    static template = 'awesome_owl.playground';
    static components = { Counter, Card };  
    setup(){
        this.state = useState({ count: 0 });
        this.incrementsum=this.incrementsum.bind(this)
    }
    incrementsum() {
        console.log('last')
        this.state.count++;
    }
}
