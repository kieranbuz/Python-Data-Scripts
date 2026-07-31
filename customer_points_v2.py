# -*- coding: utf-8 -*-
"""
Customer Loyalty Points Engine v2 — Discover Diving
Refactored 2024

Functionally identical to v1 but rewritten using vectorised Pandas
operations. Replaces manual iteration with groupby aggregation,
improving readability, performance, and scalability.
"""

import pandas as pd

POINTS_RATE = 0.025  # 2.5% of net sales


def load_data(receipts_path: str, customers_path: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    receipts = pd.read_csv(receipts_path)
    customers = pd.read_csv(customers_path)
    return receipts, customers


def calculate_points(receipts: pd.DataFrame) -> pd.DataFrame:
    return receipts.groupby('Customer name').agg(
        total_spent=('Net sales', 'sum'),
        points_balance=('Net sales', lambda x: (x * POINTS_RATE).sum()),
        total_visits=('Net sales', 'count')
    ).reset_index()


def reconcile_balances(customers: pd.DataFrame, points: pd.DataFrame) -> pd.DataFrame:
    updated = customers.merge(
        points[['Customer name', 'points_balance']],
        on='Customer name',
        how='left'
    )
    updated['Points balance'] = updated['points_balance'].fillna(0)
    return updated.drop(columns=['points_balance'])


def main():
    receipts, customers = load_data(
        "receipts-2021-12-31-2022-03-15.csv",
        "customers-2022-03-15.csv"
    )
    points = calculate_points(receipts)
    updated_customers = reconcile_balances(customers, points)
    updated_customers.to_csv("customerUpdatedPoints.csv", index=False)
    print(f"Updated points for {len(updated_customers)} customers.")


if __name__ == "__main__":
    main()
