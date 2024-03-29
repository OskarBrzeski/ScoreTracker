from datetime import datetime, timedelta, timezone

import score_tracker.api as api
import score_tracker.cli as cli
import score_tracker.database as db


def get_integer_input():
    while (result := input("Enter user ID: ")) or True:
        if not result.isnumeric():
            print(f"ERROR: {repr(result)} is not an integer.")
        elif int(result) < 1:
            print(f"ERROR: {result} must be 1 or greater.")
        else:
            break

    return result


def main():
    user_id = get_integer_input()

    ranked_maps = api.get_leaderboard_maps(
        upto=datetime(2024, 1, 1, tzinfo=timezone.utc)
    )

    ranked_maps = [map for map in ranked_maps if map.approved in ["1", "2"]]

    for i, map in enumerate(ranked_maps):
        score = api.get_score(map.beatmap_id, user_id)
        db.add_score(db._score_into_table_record(score))
        print(
            f"Progress: {i}/{len(ranked_maps)} | Time remaining {timedelta(seconds=len(ranked_maps)-i)}"
        )

    db.export_scores_as_csv(user_id)


if __name__ == "__main__":
    cli.main()
