/** @odoo-module **/

export function randomInt(max) {
    return Math.floor(Math.random() * max);
}

export function choose(array) {
    return array[randomInt(array.length)];
}
