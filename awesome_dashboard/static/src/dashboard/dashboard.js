import { Component, useState } from '@odoo/owl';
import { registry } from '@web/core/registry';
import { useService } from '@web/core/utils/hooks';
import { Layout } from '@web/search/layout';
import { DashboardItem } from './dashboard_item';

class AwesomeDashboard extends Component {
  static template = 'awesome_dashboard.AwesomeDashboard';

  static components = { Layout, DashboardItem };

  setup() {
    this.items = registry.category('awesome_dashboard.items').getAll();

    this.statisticsService = useService('statistics_service');
    this.statistics = useState(this.statisticsService.loadStatistics());
  }
}

registry
  .category('lazy_components')
  .add('awesome_dashboard.AwesomeDashboard', AwesomeDashboard);
