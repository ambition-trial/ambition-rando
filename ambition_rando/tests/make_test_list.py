import os
import csv
import random
from tempfile import mkdtemp

default_drug_assignments = ['single_dose', 'control']
default_sites = ['10', '20', '30', '40', '50']


def make_test_list(drug_assignments=None, sites=None):
    path = mkdtemp()
    drug_assignments = drug_assignments or default_drug_assignments
    sites = sites or default_sites
    filename = 'randomizationlist.csv'
    with open(os.path.join(path, 'randomizationlist.csv'), 'w') as f:
        writer = csv.DictWriter(
            f, fieldnames=['sid', 'drug_assignment', 'site'])
        writer.writeheader()
        for i in range(0, 200):
            drug_assignment = random.choice(drug_assignments)
            site = random.choice(sites)
            writer.writerow(
                dict(sid=i, drug_assignment=drug_assignment, site=site))
    return path, filename
