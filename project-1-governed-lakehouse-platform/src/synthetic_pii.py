"""Synthetic complaint and customer rows for column-mask demos.

Every row is fake. The table comment and the `data_origin` column both say so.
Do not replace Faker output with anything that looks like a real person.
"""

from __future__ import annotations

from typing import Any

from faker import Faker

COMPLAINT_PRODUCTS = (
    "checking",
    "savings",
    "mortgage",
    "credit_card",
    "auto_loan",
)
CHANNELS = ("web", "branch", "phone", "mobile")


def generate_complaints(n: int = 200, seed: int = 42) -> list[dict[str, Any]]:
    fake = Faker("en_US")
    fake.seed_instance(seed)
    rows: list[dict[str, Any]] = []
    for i in range(n):
        rows.append(
            {
                "complaint_id": f"SYN-{seed}-{i:05d}",
                "data_origin": "synthetic-faker",
                "customer_name": fake.name(),
                "ssn": fake.ssn(),
                "email": fake.email(),
                "phone": fake.phone_number(),
                "state": fake.state_abbr(),
                "product": COMPLAINT_PRODUCTS[i % len(COMPLAINT_PRODUCTS)],
                "channel": CHANNELS[i % len(CHANNELS)],
                "narrative": (
                    f"Synthetic complaint {i}: customer reports a fee dispute on "
                    f"{COMPLAINT_PRODUCTS[i % len(COMPLAINT_PRODUCTS)]}. Not a real person."
                ),
                "opened_date": fake.date_between(start_date="-400d", end_date="today").isoformat(),
            }
        )
    return rows
