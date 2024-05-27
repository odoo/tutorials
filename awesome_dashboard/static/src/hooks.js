/** @odoo-module **/

import { useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

/**
 * @returns {StatisticsStore}
 */
export const useStatistics = function () {
    return useState(useService("awesome_dashboard.statistics"));
};

/**
 * @returns {DashboardConfigStore}
 */
export const useDashboardConfig = function () {
    return useState(useService("awesome_dashboard.dashboard_config"));
};
