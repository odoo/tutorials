/** @odoo-module */

export function choose(list) {
  return list[Math.floor(Math.random() * list.length)];
}
