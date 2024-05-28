/** @odoo-module **/

import { useRef, onMounted } from "@odoo/owl";

/**
 * Focus the Dom :element:
 *
 * @param {*} element HTML Dom element t-ref to focus
 */
export function useAutofocus(element) {
  const ref = useRef(element);
  onMounted(() => ref.el.focus());
}
