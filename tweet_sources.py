import re
from collections import defaultdict
from argparse import ArgumentParser

from matplotlib import pyplot
from couchdb import Server

import settings

def get_arguments():
    parser = ArgumentParser(description="Show a graph with the tweet source popularity")

    parser.add_argument("-start", dest="start",
                        nargs="?", help="Start date in YYYY-MM-DD HH:MM format")

    parser.add_argument("-end", dest="end",
                        nargs="?", help="End date in YYYY-MM-DD HH:MM format")

    parser.add_argument("-top", default=10, type=int,
                        help="Number of the most significant sources to show")

    parser.add_argument("-pie", action="store_true", 
                        help="Show a pie chart instead")

    return parser.parse_args()

def main():
    args = get_arguments()
    
    server = Server()
    db = server = server[settings.database]

    date_pattern = r"(\d{4})-(\d{1,2})-(\d{1,2}) (\d{1,2}):(\d{2})"

    if args.start:
        date_match = re.match(date_pattern, args.start)
        if not date_match:
            print("Invalid start date format")
            exit(-1)
        start_key = [int(date_match.group(1)),
                     int(date_match.group(2)),
                     int(date_match.group(3)),
                     int(date_match.group(4)),
                     int(date_match.group(5))]
    else:
        start_key = []

    if args.end:
        date_match = re.match(date_pattern, args.end)
        if not date_match:
            print("Invalid end date format")
            exit(-1)
        end_key = [int(date_match.group(1)),
                   int(date_match.group(2)),
                   int(date_match.group(3)),
                   int(date_match.group(4)),
                   int(date_match.group(5)),{}]
    else:
        end_key = [{}]

    sources = defaultdict(int)
    url_pattern = r"<a.*?>(.*?)</a>"

    for row in db.view("tweets/sources", reduce=False, start_key=start_key, end_key=end_key):
        # if the source string contains a link, extract the text from it
        source_match = re.match(url_pattern, row.value['source'])
        if source_match: 
            sources[source_match.group(1)] += 1            
        else:
            sources[row.value['source']] += 1
 
    sorted_items = sorted(sources.items(), key=lambda x: x[1], reverse=True)
    top_items, rest = sorted_items[:args.top], sorted_items[args.top:]
    counts = [item[1] for item in top_items]
    source_types = [item[0] for item in top_items]
    other_sum = sum([item[1] for item in rest])
    counts.append(other_sum)
    source_types.append("other")

    if args.pie:
        pyplot.pie(counts, labels=source_types, autopct="%.2f%%", 
                   colors=["b", "g", "r", "c", "m", "y", "w"])
    else:
        pyplot.barh(range(len(counts)), counts, align="center")
        pyplot.yticks(range(len(counts)), source_types)
        pyplot.tight_layout()

    pyplot.show()

if __name__ == "__main__":
    main()
