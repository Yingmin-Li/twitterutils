from collections import defaultdict
from argparse import ArgumentParser

from couchdb import Server

from twitterutils.date_utils import parse_date_string
import settings

def get_arguments():
    parser = ArgumentParser(description="Show the tweets timezones")

    parser.add_argument("--start", action="store", dest="start", nargs="?",
                        help="Start date")

    parser.add_argument("--end", action="store", dest="end", nargs="?",
                        help="End date")

    return parser.parse_args()

def main():
    args = get_arguments()

    date_pattern = r"(\d{4})-(\d{1,2})-(\d{1,2}) (\d{1,2}):(\d{2})"

    if args.start:
        start_date = parse_date_string(args.start.strip())
        if not start_date:
            print("Invalid start date")
            exit(-1)
    else:
        start_date = []

    if args.end:
        end_date = parse_date_string(args.end.strip())
        if not end_date:
            print("Invalid end date")
            exit(-1)
    else:
        end_date = {}

    server = Server()
    db = server[settings.database]

    timezones = defaultdict(int)

    for row in db.view("timezones/by_date", start_key=start_date, end_key=end_date):
        timezone = row.key[-1]
        timezones[timezone] += 1

    sorted_timezones = sorted(timezones.items(), key=lambda x: x[1], reverse=True)
    
    for timezone, count in sorted_timezones:
        print timezone, count

if __name__ == "__main__":
    main()
