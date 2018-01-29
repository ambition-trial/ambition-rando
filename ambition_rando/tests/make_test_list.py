import os
import csv
import random
from tempfile import mkdtemp


default_drug_assignments = ['single_dose', 'control']


def make_test_list(full_path=None, drug_assignments=None, site_names=None,
                   count=None, first_sid=None):
    first_sid = first_sid or 0
    count = count or 50
    if not full_path:
        full_path = os.path.join(mkdtemp(), 'randomizationlist.csv')
    drug_assignments = drug_assignments or default_drug_assignments
    site_names = site_names
    with open(full_path, 'w') as f:
        writer = csv.DictWriter(
            f, fieldnames=['sid', 'drug_assignment', 'site_name'])
        writer.writeheader()
        for i in range(first_sid, count + first_sid):
            drug_assignment = random.choice(drug_assignments)
            site_name = random.choice(site_names)
            writer.writerow(
                dict(sid=i, drug_assignment=drug_assignment, site_name=site_name))
    return full_path
