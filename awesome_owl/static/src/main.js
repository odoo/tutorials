/** @odoo-module */

import { whenReady } from '@odoo/owl';
import { mountComponent } from '@web/env';
import { Playground } from './playground/playground';
import { Counter } from './counter/counter';
import { TodoList } from './todolist/todo_list';
import { Card } from './card/card';

const config = {
    dev: true,
    name: 'Owl Tutorial',
};
whenReady(() => mountComponent(TodoList, document.body, config));
