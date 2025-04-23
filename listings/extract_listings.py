import argparse
from pathlib import Path
import json
from collections import defaultdict

def parse_args(**kwargs) -> argparse.Namespace:
    parser = argparse.ArgumentParser(**kwargs)
    parser.add_argument(
        "-i", "--input",
        type = Path, default = "./abo-listings/listings/metadata",
        help = "Input listings directory path"
    )
    parser.add_argument(
        "-o", "--output",
        type = Path, default = "./metadata/listings_3d.json",
        help = "Output listings file path"
    )
    parser.add_argument(
        "-f", "--filter",
        type = str, default = "3dmodel_id",
        help = "Filter listings with the key, e.g. '3dmodel_id', 'spin_id'"
    )
    return parser.parse_args()


def load_item_listings(listings_filepath: Path) -> list:
    """Load item listings from a JSON file, one listing per line."""
    item_listings = []
    with listings_filepath.open('r') as f:
        item_listings += [json.loads(line) for line in f]
    return item_listings


def save_item_listings(item_listings: list, output_filepath: Path) -> None:
    """Save item listings to a file, one JSON object per line."""
    with output_filepath.open('w') as f:
        for listing in item_listings:
            f.write(json.dumps(listing) + '\n')


def get_item_listings(
        listings_dir: Path,
        item_filter: callable = lambda _: True,
        merge_duplicates: bool = True
    ) -> list:
    """Get listings from JSON files at given path, with optional filtering."""
    item_listings = []
    for listings_file in listings_dir.glob('*.json'):
        with listings_file.open('r') as f:
            item_listings.extend(filter(item_filter, map(json.loads, f)))

    # If multiple listings have the same Item ID, attempt to merge them
    if merge_duplicates:
        item_listings = merge_duplicate_item_listings(item_listings)

    return item_listings


def merge_duplicate_item_listings(listings: list) -> list:
    """Merge listings with duplicate Item ID."""
    item_ids = [listing['item_id'] for listing in listings]

    duplicate_listings = defaultdict(list)
    for listing in listings:
        if item_ids.count(listing['item_id']) > 1:
            duplicate_listings[ listing['item_id'] ].append(listing)
            listings.remove(listing)

    for duplicates in duplicate_listings.values():
        # Make listing with country 'US' default, if present
        for listing in duplicates:
            if listing['country'] == 'US':
                duplicates.remove(listing)
                duplicates.insert(0, listing)
                break

        # Merge listings, handling conflicts
        merged = duplicates[0]
        for listing in duplicates[1:]:
            for key, val in listing.items():
                # Check critical fields have matching values
                if key in ['item_id', 'spin_id', '3dmodel_id'] \
                    or isinstance(val, dict):
                    assert merged[key] == val, f"{key}: {merged[key]} != {val}"
                # Add new keys to merged listing
                if key not in merged:
                    merged[key] = val
                # Extend lists, excluding duplicates
                elif isinstance(val, list):
                    merged[key].extend([e for e in val if e not in merged[key]])

        listings.append(merged)
    return listings


if __name__ == "__main__":
    args = parse_args()
    item_filter = lambda listing: args.filter in listing
    model_listings = get_item_listings(args.input, item_filter=item_filter)
    save_item_listings(model_listings, args.output)
