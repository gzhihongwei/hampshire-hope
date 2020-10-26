import re
import csv
import pdfplumber

# constant fields: facilities start being listed at page 5, extra parts to delete per line, treatment types
start_page = 5
extra_parts = ['Post-detox', 'DPH', 'Second', 'Driver Alcohol', 'Offender Aftercare', 'Individual',
               'Support Services', 'Day Treatment', 'Outpatient', 'Psychopharmacological', 'Compulsive',
               'Recovery', 'MassHealth', 'for parents', 'System', 'Program']
treatment_types = ['Acute Treatment Services-Adults', 'Acute Treatment and Stabilization Services –Youth',
                   'Clinical Support Service', 'Transitional Support Service ', 'Outpatient Services',
                   'Ofﬁce-based Opioid Treatment (Buprenorphine and Vivitrol Treatment)',
                   'Opioid Treatment Programs (Methadone and Buprenorphine Treatment)', 'Residential Recovery Programs',
                   'Co-occurring Enhanced Residential Recovery Service',
                   'Jail Diversion Residential and Case Management', 'Supportive Housing',
                   'Recovery Support Services and Centers', 'Intervention and Family Support Programs',
                   'Recovery High School', 'Overdose Prevention and Syringe Access Programs',
                   'Substance Use Prevention Programs', 'Mass Opiate Abuse Prevention Collaboratives ']

# map for input
Input = {'street': 'N/A', 'city_state_zip': 'N/A', 'treatment_type': 'N/A'}

# open pdf to read from
with pdfplumber.open('facilities.pdf') as pdf:
    # start reading from start_page
    pages = pdf.pages[start_page-1:]
    with open('facility_addresses.csv', 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=Input.keys())
        w.writeheader()
        for page in pages:
            # turn page into string
            text = page.extract_text()
            # split by line and collect data needed
            for line in text.split('\n'):
                # skip page number on pdf
                if len(re.findall(r'\w+', line)) == 1 or line.find('/') != -1:
                    continue
                # record the treatment type if read
                if line in treatment_types:
                    Input['treatment_type'] = line
                if line.find(', MA') != -1 or line[0].isdigit():
                    # remove extra part then remove white spaces
                    for ele in extra_parts:
                        if ele in line:
                            line = line[:line.index(ele)]
                    line = line.strip()
                    # remove extra '-'
                    if line.endswith('-'):
                        line = line.rstrip("-")
                    # line is city/state/zip
                    if line.find(', MA') != -1:
                        # record line and input
                        Input['city_state_zip'] = line
                        w.writerow(Input)
                        # clean input to avoid error caused by missing info
                        Input['street'] = 'N/A'
                        Input['city_state_zip'] = 'N/A'
                    # line is street address
                    else:
                        # handle case with missing city/state/zip
                        if Input['street'] != 'N/A':
                            w.writerow(Input)
                        # record street address for input
                        Input['street'] = line
                        Input['city_state_zip'] = 'N/A'
