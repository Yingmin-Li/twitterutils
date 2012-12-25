import re

def parse_date_string(date_string):
    date_pattern = r"^(\d{4})-(\d{1,2})-(\d{1,2}) (\d{1,2}):(\d{2})$"

    date_match = re.match(date_pattern, date_string)

    if date_match:
        return [int(date_match.group(1)),
                int(date_match.group(2)),
                int(date_match.group(3)),
                int(date_match.group(4)),
                int(date_match.group(5))]
    else:
        return None

