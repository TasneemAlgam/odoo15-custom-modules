odoo.define('employee_expenses_portal.expenses_dashboard', function (require) {
    "use strict";

    var publicWidget = require('web.public.widget');
    var core = require('web.core');
    var _t = core._t;

    publicWidget.registry.ExpensesDashboard = publicWidget.Widget.extend({
        // selector: '#expense-nav',
        selector: '.Dashbordcontainer',
        events: {
            'click .nav-item': '_onNavItemClick',
        },
        start: function () {
            this._super.apply(this, arguments);
            this._fetchExpensesData();
        },
        _fetchExpensesData: function () {
            var self = this;
            this._rpc({
                route: '/get_expenses_data',
                params: {},
            }).then(function (data) {
                self._renderExpensesData(data);
            });
        },
        _renderExpensesData: function (data) {
            // Example logic to render data in the HTML
            var $todayList = this.$('#today-expenses ul');
            var $pastList = this.$('#past-expenses ul');
            var $summary = this.$('#expense-summary');

            $todayList.empty();
            $pastList.empty();
            $summary.empty();

            // Render Today Expenses
            data.today_expenses.forEach(function (expense) {
                $todayList.append('<li>' + expense.name + ': ' + expense.amount + '</li>');
            });

            // Render Past Expenses
            data.past_expenses.forEach(function (expense) {
                $pastList.append('<li>' + expense.name + ': ' + expense.amount + '</li>');
            });

            // Render Summary
            for (var category in data.summary) {
                $summary.append('<li>' + category + ': ' + data.summary[category] + '</li>');
            }
        },
        _onNavItemClick: function (event) {
            // Handle navigation clicks
        },
    });

    return publicWidget.registry.ExpensesDashboard;
});
