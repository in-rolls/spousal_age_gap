#!/usr/bin/env python3

import os
import sys
from argparse import ArgumentParser
from collections import namedtuple
from operator import itemgetter
from functools import partial
from Levenshtein import distance
from libs import ElectoralCSV, write_csv, ElectoralFields

APP_NAME = 'gapage'
APP_PATH = os.path.dirname(__file__)
APP_CMD = os.path.basename(__file__)
APP_VERSION = 'v1.3'
APP_DESC = '''\
Find gaps between the ages of husband and wife using parsed Electoral Roll data in CSV format created by "pdfparser" \
tool.'''

DATE_UPDATE = 'update: 19-Feb-2020'
VERSION_INFO = '{} {} ({})'.format(APP_CMD, APP_VERSION, DATE_UPDATE)
RELEASE_INFO = '''\
Release Notes:
--------------
v1.3:
  - Update output filename scheme
  - Fix a few issues.
  - Add option to +1 distance if husband name longer than 10
  - Update to working with the only selected columns to reduce memory usage.

v1.2:
  - Combined polling_station_name with household ID to be used as default searching key
  - Allowed custom of key combination via parameter --keys

v1.1:
  - Revised to adopt changes in "Gaurav_er_projects_revised_2.md"
  - Added Levenshtein distance library in replacement of similar() method

v1.0:
  - Initial version
'''

OUTFILE_ONE = os.path.join(APP_PATH, 'output/{state}_exact_match_level_{lev}.csv')
OUTFILE_MANY = os.path.join(APP_PATH, 'output/{state}_more_than_one_match_lev_{lev}.csv')
OUTFILE_ZERO = os.path.join(APP_PATH, 'output/{state}_no_match_found_lev_{lev}.csv')

DEFAULT_LD_COST = 0
DEFAULT_KEY_COMBINED = 'polling_station_name'

OutputRow = namedtuple(
    'OutputRow',
    'household_id wife_id wife_name wife_age husband_id husband_name husband_age state electoral_roll_year polling_station_name'
)


def getkey(obj, fields):
    key = ''
    for fld in fields:
        if key:
            key = '%s:%s' % (key, getattr(obj, fld))
        else:
            key = getattr(obj, fld)
    if key:
        key = '%s:%s' % (key, getattr(obj, 'house_no'))
    else:
        key = getattr(obj, 'house_no')
    return key


def get_args(*params):
    parser = ArgumentParser(description=APP_DESC, prog=APP_CMD)

    parser.add_argument('file', metavar='FILE', nargs='?', help='a CSV file parsed by pdfparser')

    parser.add_argument('--ldcost', metavar='LD_COST', type=int, default=DEFAULT_LD_COST, help='maximum Levenshtein \
distance cost accepted for matching husband name (default is %d)' % DEFAULT_LD_COST)

    parser.add_argument('--keys', metavar='KEY', nargs='+', default=[DEFAULT_KEY_COMBINED], help='list of keys will be \
used to combine with household ID in order to form a uniqueness of houses searching (by default, "%s" is used for key \
combination. Values for this param can be multiple and separated by space. Remember: should not include "house_no" \
because it\'s already included by default' % DEFAULT_KEY_COMBINED)

    parser.add_argument('--extra-ld', action='store_true', default=False, help='+1 Levenshtein \
distance if husband name length longer than 10')

    parser.add_argument('--version', action='version', version=VERSION_INFO)

    parser.add_argument('--releases', action='store_true', default=False, help='display release notes and exit')

    args = parser.parse_args(*params)

    # Return releases info
    if args.releases:
        parser.exit(message=RELEASE_INFO)

    # Check file input
    if args.file is None:
        parser.error('the following arguments are required: FILE')
    else:
        if os.path.isfile(args.file):
            if args.file[-3:].lower() not in ('csv'):
                parser.error('Not a CSV file: %s' % args.file)
        else:
            parser.error('FILE does not exist: %s' % args.file)

    # Check ldcost input
    if args.ldcost < 0:
        parser.error('LD_COST must be greater than or equal to zero')

    # Check keys combination
    if args.keys:
        if not set(args.keys).issubset(set(ElectoralFields._fields)):
            parser.error('KEYs are unknown: %s' % ', '.join(set(args.keys) - set(ElectoralFields._fields)))

    return args


def write_couples(file, couples):
    output = []
    for house, wife, husband in couples:
        if husband is None:
            kwargs = dict(husband_id='', husband_name='', husband_age='')
        else:
            kwargs = dict(husband_id=husband.id, husband_name=husband.elector_name, husband_age=husband.age)
        output.append(OutputRow(
            household_id=house,
            wife_id=wife.id,
            wife_name=wife.elector_name,
            wife_age=wife.age,
            state=wife.state,
            electoral_roll_year=wife.year,
            polling_station_name=wife.polling_station_name,
            **kwargs
        ))
    write_csv(file=file, rows=output, header=OutputRow._fields)


def main():
    args = get_args()
    print('Reading %s...' % args.file)
    parsed = ElectoralCSV(args.file)
    print('* There are %s rows in file' % len(parsed))
    print('* Found state: %s (year: %s)' % (parsed.state, parsed.year))

    houses = parsed.get_consecutive_groups(
        bykey='house_no'
    )
    print('* Found %d household IDs' % len(houses))
    print('* Finding couples...')

    couples = []
    dup_couples = []
    orphans = []
    for house, members in houses.items():
        wives = (m for m in members if m.has_husband)
        men_in_house = [m for m in members if m.refined_sex == 'male']

        for wife in wives:
            if len(men_in_house) == 0:
                # print('Zero match: %s, None' % wife.elector_name)
                orphans.append((house, wife, None))
                continue

            husband_name = wife.father_or_husband_name.lower().strip()
            ld = ((m, distance(husband_name, m.elector_name.lower().strip())) for m in men_in_house)

            cost = args.ldcost
            if args.extra_ld and len(husband_name) > 10:
                cost += 1
            candidates = sorted((i for i in ld if i[1] <= cost), key=itemgetter(1))
            # Found candidates
            if candidates:
                # Only one candidate found
                if len(candidates) == 1:
                    # print('One match: %s, %s' % (wife.elector_name, candidates[0][0].elector_name))
                    couples.append((house, wife, candidates[0][0]))
                # Many candidates found
                else:
                    lowest_cost = candidates[0][1]
                    lowest_cost_men = [i[0] for i in candidates if i[1] == lowest_cost]
                    if len(lowest_cost_men) == 1:
                        # print('One match: %s, %s' % (wife.elector_name, lowest_cost_men[0].elector_name))
                        couples.append((house, wife, lowest_cost_men[0]))
                    else:
                        for man in lowest_cost_men:
                            # print('Many match: %s, %s' % (wife.elector_name, man.elector_name))
                            dup_couples.append((house, wife, man))

            # No candidate found
            else:
                # print('Zero match: %s, None' % wife.elector_name)
                orphans.append((house, wife, None))

    print('  --> Found {} couples, {} more-than-one-match couples, {} unmatched wives'.format(
        len(couples), len(dup_couples), len(orphans)))

    print('* Writing output...')
    for data, file in [(couples, OUTFILE_ONE), (dup_couples, OUTFILE_MANY), (orphans, OUTFILE_ZERO)]:
        if data:
            file = file.format(state=parsed.state.replace(' ', '_'), lev=args.ldcost)
            write_couples(file, data)
            print('  --> %s' % file)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    except Exception as exc:
        print(exc)
        sys.exit(1)
