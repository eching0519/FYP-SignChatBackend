import csv
import os
import mysql.connector
from mysql.connector import Error
import shutil

def createCsv(collectionId, frameCount): # set the prefer number of frame   
    db = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = '',
        database = 'sign_chat'
    )
    cursor = db.cursor()

    # get data from database
    select_header = "left_0_x,left_0_y,left_0_z,left_1_x,left_1_y,left_1_z,left_2_x,left_2_y,left_2_z,left_3_x,left_3_y,left_3_z,left_4_x,left_4_y,left_4_z,left_5_x,left_5_y,left_5_z,left_6_x,left_6_y,left_6_z,left_7_x,left_7_y,left_7_z,left_8_x,left_8_y,left_8_z,left_9_x,left_9_y,left_9_z,left_10_x,left_10_y,left_10_z,left_11_x,left_11_y,left_11_z,left_12_x,left_12_y,left_12_z,left_13_x,left_13_y,left_13_z,left_14_x,left_14_y,left_14_z,left_15_x,left_15_y,left_15_z,left_16_x,left_16_y,left_16_z,left_17_x,left_17_y,left_17_z,left_18_x,left_18_y,left_18_z,left_19_x,left_19_y,left_19_z,left_20_x,left_20_y,left_20_z,right_0_x,right_0_y,right_0_z,right_1_x,right_1_y,right_1_z,right_2_x,right_2_y,right_2_z,right_3_x,right_3_y,right_3_z,right_4_x,right_4_y,right_4_z,right_5_x,right_5_y,right_5_z,right_6_x,right_6_y,right_6_z,right_7_x,right_7_y,right_7_z,right_8_x,right_8_y,right_8_z,right_9_x,right_9_y,right_9_z,right_10_x,right_10_y,right_10_z,right_11_x,right_11_y,right_11_z,right_12_x,right_12_y,right_12_z,right_13_x,right_13_y,right_13_z,right_14_x,right_14_y,right_14_z,right_15_x,right_15_y,right_15_z,right_16_x,right_16_y,right_16_z,right_17_x,right_17_y,right_17_z,right_18_x,right_18_y,right_18_z,right_19_x,right_19_y,right_19_z,right_20_x,right_20_y,right_20_z"

    sql = "SELECT signId, meaning FROM sign WHERE sign.collectionId = '"+collectionId+"'"
    cursor.execute(sql)
    rows = cursor.fetchall()

    signList = list()
    for i in rows:
        signList.append(i)

    # create csv for each sign
    for sign in signList:
        signId = sign[0]
        meaning = sign[1]
        if not os.path.exists('./ai_csv/'+collectionId+'/'+meaning):
            os.makedirs('./ai_csv/'+collectionId+'/'+meaning)
            
        signId = str(signId)
        sql = 'SELECT '+select_header+' FROM frame WHERE signId = '+signId+' ORDER BY sequenceNo'
        cursor.execute(sql)
        frameRows = cursor.fetchall()

        headers = [col[0] for col in cursor.description]

        # create csv file from data
        fp = open('./ai_csv/'+collectionId+'/'+meaning+'/'+signId+'.csv', 'w')
        my_csv = csv.writer(fp,lineterminator = '\n')
        my_csv.writerow(headers)

        csv_rows = []
        

        if ( float(frameCount) / len(frameRows)) <= 1:
            extendRatio = int(frameCount / len(frameRows))
        else:
            extendRatio = round(frameCount / len(frameRows))
        
        if extendRatio >= 1:
            for frameRow in frameRows:
                for i in range(extendRatio):
                    csv_row = []
                    for cell in frameRow:
                        if cell==None:
                            csv_row.append(-99.99)
                        else:
                            csv_row.append(cell)
                    csv_rows.append(csv_row)
        else:
            compressRatio = round(len(frameRows) / frameCount)
            index = 0
            for frameRow in frameRows:
                if index % compressRatio == 0:
                    csv_row = []
                    for cell in frameRow:
                        if cell==None:
                            csv_row.append(-99.99)
                        else:
                            csv_row.append(cell)
                    csv_rows.append(csv_row)
                index += 1

        my_csv.writerows(csv_rows)
        fp.close()

def removeCsv(collectionId):
    shutil.rmtree('./ai_csv/'+collectionId)
    print("CSV files removed.")