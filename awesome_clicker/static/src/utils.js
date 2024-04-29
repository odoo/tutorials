/** @odoo-module **/

export function choose(array) {
    return array[Math.floor(Math.random()*array.length)];
}