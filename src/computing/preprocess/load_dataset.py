import pandas as pd
import os, glob
from ..utils import db
from os.path import basename

def load():
    print ("\nLoading dataset into db...")

    # Change directory to the script directory
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    dataset_dir = '../../../dataset/csv/'

    conn = db.get_conn()

    # Load every csv file in a separate table
    for file in glob.glob(dataset_dir + '*.csv'):
        data_frame = pd.read_csv(file)
        table_name = os.path.splitext(basename(file))[0]
        data_frame.to_sql(table_name, conn, if_exists='replace', index=False)

    conn.commit()

    # Fix not unique sensors into OrdonezB_Sensors dataset
    # (e.g Door Kitchen, Door Bedroom, Door Bathroom, Door Living)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM OrdonezB_Sensors AS O WHERE O.location LIKE "Door"')
    rows = cursor.fetchall()
    for row in rows:
        fixed_location = row[2] + '_' + row[4]
        cursor.execute('UPDATE OrdonezB_Sensors SET location = ? WHERE start_time = ? AND end_time = ?', [fixed_location, row[0], row[1]])

    conn.commit()
    conn.close()

    print ("\nDataset loaded! :)")
