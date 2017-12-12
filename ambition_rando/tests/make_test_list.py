import os
import csv
import random
from tempfile import mkdtemp

default_drug_assignments = ['single_dose', 'control']
default_sites = ['10', '20', '30', '40', '50']


def make_test_list(drug_assignments=None, sites=None, count=None, first_sid=None):
    first_sid = first_sid or 0
    count = count or 50
    path = mkdtemp()
    drug_assignments = drug_assignments or default_drug_assignments
    sites = sites or default_sites
    filename = 'randomizationlist.csv'
    with open(os.path.join(path, 'randomizationlist.csv'), 'w') as f:
        writer = csv.DictWriter(
            f, fieldnames=['sid', 'drug_assignment', 'site'])
        writer.writeheader()
        for i in range(first_sid, count + first_sid):
            drug_assignment = random.choice(drug_assignments)
            site = random.choice(sites)
            writer.writerow(
                dict(sid=i, drug_assignment=drug_assignment, site=site))
    return path, filename
