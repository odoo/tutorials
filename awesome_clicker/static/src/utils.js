/** @odoo-module **/

/*
Returns a random integer between min and max
The maximum and the minimum are inclusive
*/
export function randomInt(min, max) {
    const minCeiled = Math.ceil(min);
    const maxFloored = Math.floor(max);
    return Math.floor(Math.random() * (maxFloored - minCeiled + 1) + minCeiled);
}

/*
Returns an element chosen randomly in the array
The choice is made with a uniform law
*/
export function choose(array) {
    return array[randomInt(0, array.length-1)];
}
