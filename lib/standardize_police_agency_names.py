'''Utility to standardize police agency/department names across datasets.

Author: Everett Wetchler (everett.wetchler@gmail.com)
'''

MISSPELLINGS = {
    'ATTYS': 'ATTY',
    'FAMERS': 'FARMERS',
    'BELVILLE': 'BELLVILLE',
}
for keyword in ('DEPARTMENT', 'SHERIFFS', 'MARSHALS', 'ATTORNEY'):
    no_s = keyword.rstrip('S')
    MISSPELLINGS[no_s] = keyword
    MISSPELLINGS[keyword + 'S'] = keyword
    for i in range(len(no_s)):
        # Failed to pluralize
        mistakes = []
        # Letter missing
        mistakes.append(no_s[:i] + no_s[(i+1):])
        # Letter duplicated
        mistakes.append(no_s[:i] + no_s[i] + no_s[i:])
        for m in mistakes:
            MISSPELLINGS[m] = keyword
            MISSPELLINGS[m + 'S'] = keyword


ABBREVIATIONS = {
    'DEPARTMENT': 'DEPT',
    'DISTRICT': 'DIST',
    'COUNTY': 'CO',
    'STATE': 'ST',
    'UNIVERSITY': 'UNIV',
    'ATTORNEY': 'ATTY',
    'ATTORNEYS': 'ATTY',
    'AUTHORITY': 'AUTH',
    'PRECINCT': 'PCT',
    'CONSTABLE': 'CONST',
    'CONSTABLES': 'CONST',
}


MULTIWORD_RENAMINGS = {
    "CONST OFFICE": "CONST",
    "SHERIFFS DEPT": "SHERIFFS OFFICE",
    'CITY OF': '',
}


MANUAL_RENAMINGS = {
    "DART POLICE DEPT": "DALLAS AREA RAPID TRANSIT POLICE DEPT",
    "DART": "DALLAS AREA RAPID TRANSIT POLICE DEPT",
    "CITY MARSHAL OF MARSHALL, TEXAS": "MARSHALL MARSHALS OFFICE",
    "TEXAS DEPT OF PUBLIC SAFETY CRIMINAL INVESTIGATIONS DIVISION": "TEXAS DEPT OF PUBLIC SAFETY",
    "ALAMO COMMUNITY COLLEGE DIST.": "ALAMO COMMUNITY COLLEGE DIST POLICE DEPT",
}


def reorder_parts(parts):
    # Move precinct number(s) to the end, if applicable
    for i, p in enumerate(parts):
        if p == 'PCT':
            j = i + 1
            while j < len(parts) and (parts[j].isdigit() or parts[j] in ('&', 'AND')):
                j += 1
            parts = parts[:i] + parts[j:] + parts[i:j]
            break
    return parts


def has_alnum(word):
    return any(ch for ch in word if ch.isalnum())


def clean_punct(word):
    # Remove all punctuation EXCEPT internal dashes
    word = ''.join(ch for ch in word if ch.isalnum() or ch == '-')
    if word == '-':
        return ''
    return word


def standardize_agency_name(agency):
    if not isinstance(agency, str):
        return None
    # Remove whitespace and uppercase
    agency = agency.strip().upper()
    if agency in MANUAL_RENAMINGS:
        return MANUAL_RENAMINGS[agency]
    parts = agency.split()
    parts = [clean_punct(p) for p in parts]
    parts = [p for p in parts if p]
    parts = [MISSPELLINGS.get(p, p) for p in parts]
    parts = [ABBREVIATIONS.get(p, p) for p in parts]
    parts = reorder_parts(parts)
    agency = ' '.join(parts)
    for before, after in MULTIWORD_RENAMINGS.items():
        agency = agency.replace(before, after)
    agency = ' '.join([p for p in agency.split() if p and p != '-'])
    if agency.endswith('MARSHALS') or agency.endswith('SHERIFFS'):
        agency = agency + ' OFFICE'
    return agency
