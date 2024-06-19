/** @odoo-module **/

import { onMounted, useRef } from "@odoo/owl";

export type InputRef = ReturnType<typeof useRef<HTMLInputElement>>;

export const useAutofocus = (ref: InputRef) => {
  onMounted(() => {
    ref.el?.focus();
  });
};
