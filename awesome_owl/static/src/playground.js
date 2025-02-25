/** @odoo-module **/

import { Component, useState } from '@odoo/owl';
import {Card} from './card/card';

export class Playground extends Component {
    static template = 'awesome_owl.playground';
    static components = { Card };

    setup() {
        this.totalCount = useState(
            {
                value: 0
            }
        );
    };

    incrementTotalCount() {
        this.totalCount.value++;
    }
}
