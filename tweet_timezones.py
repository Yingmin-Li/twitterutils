from collections import defaultdict
from argparse import ArgumentParser

from couchdb import Server
from matplotlib import pyplot

from twitterutils.date_utils import parse_date_string
import settings

def get_arguments():
    parser = ArgumentParser(description="Show the tweets timezones")

    parser.add_argument("--start", action="store", dest="start", nargs="?",
                        help="Start date")

    parser.add_argument("--end", action="store", dest="end", nargs="?",
                        help="End date")

    parser.add_argument("--top", type=int, default=10, action="store", dest="top",
                        help="The maximum number of timezones to display")

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
        timezones[row.value['timezone']] += 1

    sorted_timezones = sorted(timezones.items(), key=lambda x: x[1], reverse=True)
    
    top_timezones, rest_timezones = sorted_timezones[:args.top], sorted_timezones[args.top:]
    
    counts = [timezone[1] for timezone in top_timezones]
    labels = [timezone[0] for timezone in top_timezones]

    rest_sum = sum([timezone[1] for timezone in rest_timezones])
    counts.append(rest_sum)

    labels.append("Other")

    pyplot.barh(range(len(counts)), counts, align="center")
    pyplot.yticks(range(len(counts)), labels)
    pyplot.tight_layout()
    pyplot.show()

if __name__ == "__main__":
    main()
