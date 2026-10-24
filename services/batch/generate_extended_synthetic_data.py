"""Extended synthetic data generator for InstaMart retail and advertisement analytics.

This script generates configurable synthetic retail transactions and advertisement data
with reproducible timestamps, products, customers, campaigns, impressions, clicks,
conversions, spend, and revenue. All data is clearly labeled as synthetic.

Scalable to millions of records with fixed random seeds for reproducibility.
"""

from __future__ import annotations

import argparse
import csv
import random
import hashlib
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Iterable, List, Dict, Set


@dataclass(frozen=True)
class Product:
    """Represents a product in the retail catalogue."""
    product_id: str
    name: str
    category: str
    min_price: float
    max_price: float

    def sample_price(self) -> float:
        price = random.uniform(self.min_price, self.max_price)
        return round(price, 2)


@dataclass(frozen=True)
class Customer:
    """Represents a customer."""
    customer_id: str
    segment: str
    city: str


@dataclass(frozen=True)
class Campaign:
    """Represents an advertisement campaign."""
    campaign_id: str
    name: str
    platform: str
    daily_budget: float


# Product catalogue (expanded from original)
PRODUCTS: List[Product] = [
    Product("P001", "Masala Dosa", "Food", 80.0, 140.0),
    Product("P002", "Paneer Tikka Wrap", "Food", 120.0, 180.0),
    Product("P003", "Vegetable Biryani", "Food", 150.0, 220.0),
    Product("P004", "Idli Sambar Combo", "Food", 60.0, 110.0),
    Product("P005", "Chole Bhature", "Food", 90.0, 150.0),
    Product("P006", "Pav Bhaji", "Food", 80.0, 130.0),
    Product("P007", "Vegetable Pulao", "Food", 110.0, 170.0),
    Product("P008", "Paneer Butter Masala", "Food", 180.0, 260.0),
    Product("P009", "Mango Lassi", "Beverage", 70.0, 120.0),
    Product("P010", "Filter Coffee", "Beverage", 40.0, 80.0),
    Product("P011", "Masala Chai", "Beverage", 25.0, 60.0),
    Product("P012", "Gulab Jamun Pack", "Dessert", 90.0, 140.0),
    Product("P013", "Vegetable Sandwich", "Food", 50.0, 90.0),
    Product("P014", "Ragi Millet Bowl", "Food", 130.0, 190.0),
    Product("P015", "Pani Puri Kit", "Food", 60.0, 110.0),
    Product("P016", "Samosa Pack", "Food", 40.0, 80.0),
    Product("P017", "Fresh Fruit Juice", "Beverage", 60.0, 100.0),
    Product("P018", "Mixed Veg Platter", "Food", 200.0, 300.0),
    Product("P019", "Dal Makhani", "Food", 140.0, 200.0),
    Product("P020", "Naan Bread", "Food", 30.0, 60.0),
]

# Customer segments
CUSTOMER_SEGMENTS = ["Premium", "Regular", "Budget"]
CITIES = [
    "Bengaluru", "Delhi", "Mumbai", "Chennai", "Hyderabad",
    "Kolkata", "Pune", "Ahmedabad", "Jaipur", "Lucknow"
]

# Advertisement campaigns
CAMPAIGNS: List[Campaign] = [
    Campaign("C001", "Summer Sale 2024", "Facebook", 5000.0),
    Campaign("C002", "Weekend Brunch Promo", "Instagram", 3000.0),
    Campaign("C003", "Healthy Choices", "Google Ads", 4000.0),
    Campaign("C004", "Quick Meals", "Twitter", 2000.0),
    Campaign("C005", "Festival Special", "Facebook", 6000.0),
    Campaign("C006", "New Product Launch", "Instagram", 4500.0),
    Campaign("C007", "Loyalty Rewards", "Email", 1500.0),
    Campaign("C008", "Bundle Deals", "Google Ads", 3500.0),
]

# Store locations (from original)
STORES = [
    ("BLR-01", "Bengaluru - Indiranagar"),
    ("BLR-02", "Bengaluru - Koramangala"),
    ("DEL-01", "Delhi - Connaught Place"),
    ("DEL-02", "Delhi - Saket"),
    ("MUM-01", "Mumbai - Bandra"),
    ("MUM-02", "Mumbai - Powai"),
    ("CHE-01", "Chennai - T Nagar"),
    ("CHE-02", "Chennai - Velachery"),
    ("HYD-01", "Hyderabad - Banjara Hills"),
    ("HYD-02", "Hyderabad - Gachibowli"),
]


def generate_customers(num_customers: int, seed: int) -> List[Customer]:
    """Generate deterministic customers."""
    random.seed(seed)
    customers = []
    for i in range(num_customers):
        customer_id = f"CUST{i+1:06d}"
        segment = random.choice(CUSTOMER_SEGMENTS)
        city = random.choice(CITIES)
        customers.append(Customer(customer_id, segment, city))
    return customers


def daterange(start: datetime, days: int) -> Iterable[datetime]:
    """Generate datetime range."""
    for offset in range(days):
        yield start + timedelta(days=offset)


def generate_retail_record(
    day: datetime,
    seq: int,
    customers: List[Customer],
    products: List[Product],
    stores: List[tuple[str, str]]
) -> Dict:
    """Generate a single retail transaction record."""
    product = random.choice(products)
    quantity = random.randint(1, 5)
    unit_price = product.sample_price()

    # Occasional promotional discounts
    discount_factor = random.choice([1.0, 1.0, 1.0, 0.9, 0.95])
    unit_price = round(unit_price * discount_factor, 2)
    total = round(unit_price * quantity, 2)

    customer = random.choice(customers)
    store_id, store_city = random.choice(stores)

    # Generate timestamp within the day
    hour = random.randint(6, 22)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    timestamp = day.replace(hour=hour, minute=minute, second=second)

    order_id = f"{day.strftime('%Y%m%d')}-{seq:06d}"

    return {
        "data_source": "SYNTHETIC_RETAIL",
        "order_id": order_id,
        "order_timestamp": timestamp.isoformat(),
        "order_date": day.strftime("%Y-%m-%d"),
        "customer_id": customer.customer_id,
        "customer_segment": customer.segment,
        "customer_city": customer.city,
        "store_id": store_id,
        "store_city": store_city,
        "product_id": product.product_id,
        "product_name": product.name,
        "product_category": product.category,
        "quantity": quantity,
        "unit_price": f"{unit_price:.2f}",
        "amount": f"{total:.2f}",
    }


def generate_ad_record(
    day: datetime,
    seq: int,
    customers: List[Customer],
    products: List[Product],
    campaigns: List[Campaign]
) -> Dict:
    """Generate a single advertisement event record."""
    campaign = random.choice(campaigns)
    product = random.choice(products)
    customer = random.choice(customers)

    # Generate timestamp within the day
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    timestamp = day.replace(hour=hour, minute=minute, second=second)

    event_id = f"ADV-{day.strftime('%Y%m%d')}-{seq:06d}"

    # Simulate ad interaction funnel
    has_impression = True
    has_click = random.random() < 0.05  # 5% click-through rate
    has_conversion = has_click and random.random() < 0.20  # 20% conversion on click

    spend_per_impression = campaign.daily_budget / 10000.0  # Avg cost per impression
    spend = round(spend_per_impression, 4)

    revenue = 0.0
    if has_conversion:
        revenue = round(random.uniform(50.0, 300.0), 2)

    return {
        "data_source": "SYNTHETIC_ADVERTISEMENT",
        "event_id": event_id,
        "event_timestamp": timestamp.isoformat(),
        "event_date": day.strftime("%Y-%m-%d"),
        "customer_id": customer.customer_id,
        "customer_segment": customer.segment,
        "customer_city": customer.city,
        "campaign_id": campaign.campaign_id,
        "campaign_name": campaign.name,
        "platform": campaign.platform,
        "product_id": product.product_id,
        "product_name": product.name,
        "product_category": product.category,
        "impressions": 1 if has_impression else 0,
        "clicks": 1 if has_click else 0,
        "conversions": 1 if has_conversion else 0,
        "spend": f"{spend:.4f}",
        "revenue": f"{revenue:.2f}",
    }


def generate_data_files(
    output_dir: Path,
    days: int,
    transactions_per_day: int,
    ad_events_per_day: int,
    start_date: datetime,
    customers: List[Customer],
    products: List[Product],
    stores: List[tuple[str, str]],
    campaigns: List[Campaign],
) -> List[Path]:
    """Generate retail and advertisement data files."""
    generated_files = []

    retail_rows = []
    ad_rows = []

    for day_idx, day in enumerate(daterange(start_date, days)):
        # Generate retail records
        for seq in range(transactions_per_day):
            record = generate_retail_record(
                day,
                day_idx * transactions_per_day + seq,
                customers,
                products,
                stores
            )
            retail_rows.append(record)

        # Generate advertisement records
        for seq in range(ad_events_per_day):
            record = generate_ad_record(
                day,
                day_idx * ad_events_per_day + seq,
                customers,
                products,
                campaigns
            )
            ad_rows.append(record)

    # Write retail data
    retail_path = output_dir / "synthetic_retail_data.csv"
    with retail_path.open("w", newline="", encoding="utf-8") as fh:
        if retail_rows:
            writer = csv.DictWriter(fh, fieldnames=list(retail_rows[0].keys()))
            writer.writeheader()
            writer.writerows(retail_rows)
    generated_files.append(retail_path)

    # Write advertisement data
    ad_path = output_dir / "synthetic_advertisement_data.csv"
    with ad_path.open("w", newline="", encoding="utf-8") as fh:
        if ad_rows:
            writer = csv.DictWriter(fh, fieldnames=list(ad_rows[0].keys()))
            writer.writeheader()
            writer.writerows(ad_rows)
    generated_files.append(ad_path)

    return generated_files


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate extended synthetic retail and advertisement data"
    )
    parser.add_argument(
        "--output",
        default="/opt/spark-data/input",
        help="Directory for generated CSV files"
    )
    parser.add_argument(
        "--days",
        type=int,
        default=30,
        help="Number of days to generate data for"
    )
    parser.add_argument(
        "--transactions-per-day",
        type=int,
        default=1000,
        help="Retail transactions per day"
    )
    parser.add_argument(
        "--ad-events-per-day",
        type=int,
        default=2000,
        help="Advertisement events per day"
    )
    parser.add_argument(
        "--num-customers",
        type=int,
        default=10000,
        help="Number of unique customers to generate"
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=2024,
        help="Random seed for reproducibility"
    )
    parser.add_argument(
        "--start-date",
        help="Start date (YYYY-MM-DD). Defaults to days ending today."
    )
    parser.add_argument(
        "--keep-existing",
        action="store_true",
        help="Do not delete pre-existing CSV files in the output directory"
    )
    return parser.parse_args()


def determine_start_date(days: int, explicit: str | None) -> datetime:
    if explicit:
        try:
            return datetime.strptime(explicit, "%Y-%m-%d")
        except ValueError as exc:
            raise SystemExit(f"Invalid --start-date '{explicit}': {exc}")

    today = datetime.now()
    return today - timedelta(days=days - 1)


def _ensure_output_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def _clear_existing_files(path: Path, *, extension: str = ".csv") -> None:
    for file in path.glob(f"*{extension}"):
        file.unlink()


def main() -> None:
    args = parse_args()
    random.seed(args.seed)

    output_dir = Path(args.output)
    _ensure_output_dir(output_dir)

    if not args.keep_existing:
        _clear_existing_files(output_dir)

    start_day = determine_start_date(args.days, args.start_date)

    # Generate customers
    customers = generate_customers(args.num_customers, args.seed)

    # Generate data files
    generated_files = generate_data_files(
        output_dir,
        args.days,
        args.transactions_per_day,
        args.ad_events_per_day,
        start_day,
        customers,
        PRODUCTS,
        STORES,
        CAMPAIGNS,
    )

    total_retail_records = args.days * args.transactions_per_day
    total_ad_records = args.days * args.ad_events_per_day
    total_records = total_retail_records + total_ad_records

    print(f"Generated {len(generated_files)} file(s) under {output_dir}")
    print(f"Total records: {total_records:,}")
    print(f"  - Retail transactions: {total_retail_records:,}")
    print(f"  - Advertisement events: {total_ad_records:,}")
    print(f"  - Unique customers: {len(customers):,}")
    print(f"  - Date range: {start_day.strftime('%Y-%m-%d')} to {(start_day + timedelta(days=args.days-1)).strftime('%Y-%m-%d')}")
    for path in generated_files:
        print(f" - {path.name}")


if __name__ == "__main__":
    main()
