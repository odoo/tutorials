/** @odoo-module **/

import { registry } from "@web/core/registry";
import { reactive } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { Component, useState, useExternalListener } from "@odoo/owl";

export function useClicker() {
    return useState(useService("awesome_clicker.clicker_service"));
}
