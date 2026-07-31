# -*- coding: utf-8 -*-
"""
Customer Loyalty Points Engine v1 — Discover Diving
Deployed: March 2022

Aggregates transaction data from POS receipts export, calculates
spend-based loyalty points at 2.5% of net sales, and reconciles
balances across the full customer database.
"""

import pandas as pd

receipts = pd.read_csv("receipts-2021-12-31-2022-03-15.csv")
customers = pd.read_csv("customers-2022-03-15.csv")

temp = pd.DataFrame(columns=['Customer name', 'Total spent', 'Points balance', 'Total visits'])

customerName = []
for ind in receipts.index:
    if receipts['Customer name'][ind] in customerName:
        continue
    else:
        customerName.append(receipts['Customer name'][ind])

temp['Customer name'] = customerName

totalSales = [0] * len(customerName)
for ind in receipts.index:
    index = customerName.index(receipts['Customer name'][ind])
    totalSales[index] = totalSales[index] + receipts['Net sales'][ind]

temp['Total spent'] = totalSales

totalSales = [0] * len(customerName)
for ind in receipts.index:
    index = customerName.index(receipts['Customer name'][ind])
    totalSales[index] = totalSales[index] + (receipts['Net sales'][ind] * 0.025)

temp['Points balance'] = totalSales

totalVisits = [0] * len(customerName)
for ind in receipts.index:
    index = customerName.index(receipts['Customer name'][ind])
    totalVisits[index] = totalVisits[index] + 1

temp['Total visits'] = totalVisits

for ind in customers.index:
    if customers['Customer name'][ind] in customerName:
        index = customerName.index(customers['Customer name'][ind])
        customers.loc[ind, 'Points balance'] = temp['Points balance'][index]
    else:
        customers.loc[ind, 'Points balance'] = 0

customers.to_csv("customerUpdatedPoints.csv")
