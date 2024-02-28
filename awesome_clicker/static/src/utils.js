/** @odoo-module */

export const chooseReward = (array) => {
    const random_element = Math.floor(Math.random() * array.length);
    return array[random_element];
}