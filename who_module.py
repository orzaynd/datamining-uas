import pandas as pd

# HAZ
haz_boys_0_2 = pd.read_excel(
    "who_data/lhfa_boys_0-to-2-years_zscores.xlsx"
)

haz_boys_2_5 = pd.read_excel(
    "who_data/lhfa_boys_2-to-5-years_zscores.xlsx"
)

haz_girls_0_2 = pd.read_excel(
    "who_data/lhfa_girls_0-to-2-years_zscores.xlsx"
)

haz_girls_2_5 = pd.read_excel(
    "who_data/lhfa_girls_2-to-5-years_zscores.xlsx"
)

# WAZ
waz_boys = pd.read_excel(
    "who_data/wfa_boys_0-to-5-years_zscores.xlsx"
)

waz_girls = pd.read_excel(
    "who_data/wfa_girls_0-to-5-years_zscores.xlsx"
)

# WHZ
whz_boys = pd.read_excel(
    "who_data/wfh_boys_2-to-5-years_zscores.xlsx"
)

whz_girls = pd.read_excel(
    "who_data/wfh_girls_2-to-5-years_zscores.xlsx"
)

def calculate_haz_zscore(age_month, height_cm, haz_table):

    row = haz_table[haz_table['Month'] == age_month]

    if len(row) == 0:
        return None

    row = row.iloc[0]

    points = [
        (row['SD3neg'], -3),
        (row['SD2neg'], -2),
        (row['SD1neg'], -1),
        (row['SD0'], 0),
        (row['SD1'], 1),
        (row['SD2'], 2),
        (row['SD3'], 3)
    ]

    for i in range(len(points)-1):

        x1, z1 = points[i]
        x2, z2 = points[i+1]

        if x1 <= height_cm <= x2:

            zscore = z1 + (
                (height_cm - x1)
                * (z2 - z1)
                / (x2 - x1)
            )

            return round(float(zscore), 2)

    if height_cm < row['SD3neg']:
        return -3.0

    if height_cm > row['SD3']:
        return 3.0

    return None

def get_haz_status(age_month, height_cm, haz_table):

    row = haz_table[haz_table['Month'] == age_month]

    if len(row) == 0:
        return None

    row = row.iloc[0]

    if height_cm < row['SD3neg']:
        return "Severely Stunted"

    elif height_cm < row['SD2neg']:
        return "Stunted"

    else:
        return "Normal"
    
def get_haz_table(gender, age_month):

    if gender == "Male":

        if age_month <= 24:
            return haz_boys_0_2
        else:
            return haz_boys_2_5

    else:

        if age_month <= 24:
            return haz_girls_0_2
        else:
            return haz_girls_2_5
        
def calculate_waz_zscore(age_month, weight_kg, waz_table):

    row = waz_table[waz_table['Month'] == age_month]

    if len(row) == 0:
        return None

    row = row.iloc[0]

    points = [
        (row['SD3neg'], -3),
        (row['SD2neg'], -2),
        (row['SD1neg'], -1),
        (row['SD0'], 0),
        (row['SD1'], 1),
        (row['SD2'], 2),
        (row['SD3'], 3)
    ]

    for i in range(len(points)-1):

        x1, z1 = points[i]
        x2, z2 = points[i+1]

        if x1 <= weight_kg <= x2:

            zscore = z1 + (
                (weight_kg - x1)
                * (z2 - z1)
                / (x2 - x1)
            )

            return round(float(zscore), 2)

    if weight_kg < row['SD3neg']:
        return -3.0

    if weight_kg > row['SD3']:
        return 3.0

    return None

def get_waz_status(zscore):

    if zscore < -3:
        return "Severely Underweight"

    elif zscore < -2:
        return "Underweight"

    else:
        return "Normal"
    
def get_waz_table(gender):

    if gender == "Male":
        return waz_boys
    else:
        return waz_girls
    
def calculate_whz_zscore(height_cm, weight_kg, whz_table):

    idx = (whz_table['Height'] - height_cm).abs().idxmin()

    row = whz_table.loc[idx]

    points = [
        (row['SD3neg'], -3),
        (row['SD2neg'], -2),
        (row['SD1neg'], -1),
        (row['SD0'], 0),
        (row['SD1'], 1),
        (row['SD2'], 2),
        (row['SD3'], 3)
    ]

    for i in range(len(points)-1):

        x1, z1 = points[i]
        x2, z2 = points[i+1]

        if x1 <= weight_kg <= x2:

            zscore = z1 + (
                (weight_kg - x1)
                * (z2 - z1)
                / (x2 - x1)
            )

            return round(float(zscore), 2)

    if weight_kg < row['SD3neg']:
        return -3.0

    if weight_kg > row['SD3']:
        return 3.0

    return None

def get_whz_status(zscore):

    if zscore < -3:
        return "Severely Wasted"

    elif zscore < -2:
        return "Wasted"

    elif zscore <= 2:
        return "Normal"

    else:
        return "Overweight"
    

def get_whz_table(gender):

    if gender == "Male":
        return whz_boys
    else:
        return whz_girls

print("WHO tables loaded")