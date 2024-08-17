# -*- coding: utf-8 -*-

from collections import OrderedDict
from collections import defaultdict 

from odoo import http, _
from odoo.http import request
from odoo.addons.portal.controllers.portal import pager as portal_pager, CustomerPortal
from datetime import datetime
import json

class EmployeeExpensesPortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        """Employee Expenses's in home portal"""
        user = request.env.user
        values = super()._prepare_home_portal_values(counters)
        if 'my_expense_count' in counters:
            values['my_expense_count'] = request.env[
                'hr.expense'].search_count(
                [('employee_id.user_id.id', '=', user.id)]) if request.env[
                'hr.expense'].check_access_rights(
                'read', raise_exception=False) else 0
        return values

    def _emp_expense_get_page_view_values(self, employee_expense, access_token, **kwargs):
        """Employee Expenses Page values"""
        values = {
            'page_name': 'employee_expense',
            'employee_expense': employee_expense,
        }
        return self._get_page_view_values(employee_expense, access_token, values,
                                          'my_expenses_history', False, **kwargs)

    @http.route(['/my/employee_expenses', '/my/employee_expenses/page/<int:page>'],
                type='http', auth="public", website=True)
    def portal_my_employee_expenses(self, page=1, date_begin=None,
                              date_end=None, sortby=None, filterby=None, **kw):
        """Portal Employee Expenses"""
        values = self._prepare_portal_layout_values()
        user = request.env.user
        employee_expenses = request.env['hr.expense'].search([])
        for x in employee_expenses:
            print('ggggg',x.date)
        domain = [
            ('employee_id.user_id.id', '=', user.id), ('state', 'not in', ['draft'])]
        exp_count = employee_expenses.search_count(domain)
        
        pager = portal_pager(
            url="/my/employee_expenses",
            url_args={'date_begin': date_begin, 'date_end': date_end,
                      'sortby': sortby, 'filterby': filterby},
            total=exp_count,
            page=page,
            step=self._items_per_page
        )

        expenses = employee_expenses.search(
            domain,
            # order=order,
            limit=self._items_per_page,
            offset=pager['offset']
        )
        today = datetime.now().date()
        # Get expenses for today
        today_expenses = request.env['hr.expense'].search([('employee_id.user_id.id', '=', user.id),('date', '=', datetime.now().date())])
        # Get expenses older
        older_expenses = request.env['hr.expense'].search([('employee_id.user_id.id', '=', user.id),('date', '<', datetime.now().date())])
        # Group expenses by date and calculate totals
        expenses_by_date=employee_expenses.search([('employee_id.user_id.id', '=', user.id),
            ('date', '!=', False)])
        expenses_grouped = defaultdict(float)
        chart_max_total = max(record['total_amount'] for record in expenses_by_date) if expenses_by_date else 1
        chart_data = []
        for record in expenses_by_date:
            date_key = record.date.strftime('%Y-%m-%d')  
            height = (record['total_amount'] / chart_max_total) * 100
            expenses_grouped[date_key] += record.total_amount
        chart_data = sorted(
            [{'date': date, 'total_amount': amount,'height':(amount/ chart_max_total) * 100} for date, amount in expenses_grouped.items()],
            key=lambda x: x['date'], reverse=False
        )
        # Group expenses by product and calculate totals, filtering by user_id
        expenses_product_grouped = request.env['hr.expense'].read_group(
            [('employee_id.user_id.id', '=', user.id), ('date', '!=', False)],  
            ['product_id', 'total_amount:sum'],  
            ['product_id']  
        )
        product_max_total = max(record['total_amount'] for record in expenses_product_grouped) if expenses_product_grouped else 1
        progress_bar_data = []
        for record in expenses_product_grouped:
            product = request.env['product.product'].search([('id', '=', record['product_id'][0])]).name
            date_str = product
            height = (record['total_amount'] / product_max_total) * 100
            progress_bar_data.append({'label': date_str, 'height': height, 'total_amount': record['total_amount']})


        values.update({
            'expenses': employee_expenses,
            'today_expenses': today_expenses,
            'older_expenses': older_expenses,
            'chart_data': chart_data,
            'progress_bar_data': progress_bar_data,
            'page_name': 'employee_expense',
            'pager': pager,
            'default_url': '/my/employee_expenses',
        })
        return request.render(
            "employee_expenses_portal.portal_my_expense",
            values)
