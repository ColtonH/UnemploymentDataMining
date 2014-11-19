# Author: M.A. Menarguez

from openpyxl import load_workbook
from openpyxl.cell import get_column_letter
import os
#from data.models import UsState,UnemploymentByStateMonthly

def getFilesInDir(path,ext):
    files=[]
    for f in os.listdir(path):
        if f.endswith("."+str(ext)):
            files.append(f)
    return files

def retrieve_data(path,files):
    data = {}
    for f in files:
        wb = load_workbook(path+'/'+f)
        sheet_name = wb.get_sheet_names()[0]
        sheet_ranges = wb[sheet_name]
        row = 1;
        while (True):
            row += 1
            state = sheet_ranges['B'+str(row)].value
            if (not state or state==""):
                break
            year = int(sheet_ranges['D'+str(row)].value)
            race =  sheet_ranges['F'+str(row)].value
            births =  int(sheet_ranges['H'+str(row)].value)
            birth_rate = sheet_ranges['J'+str(row)]
            if birth_rate.value:
                birth_rate = float(sheet_ranges['J'+str(row)].value)
            if state not in data.keys():
                data[state]={}
            if year not in data[state].keys():
                data[state][year]={}
            data[state][year][race] = {
                'births': births,
                'birth_rate' : birth_rate
            }
    return data



def insert_unemployment_state(state,state_data):
    # Check if state exists
    print "Inserting "+ state
    try:
        state = UsState.objects.get(name=state)
    except Exception, e:
        # State does not exit, need to add it to the list
        state = UsState(name=state)
        try:
            state.save()
        except Exception, e:
            # Unhandled error
            print "Error adding state: "+state
            print "Exit..." 
            sys.exit(0)
    # Add all data
    for year in state_data.keys():
        # print year
        for month in range(0,len(state_data[year])):
            if state_data[year][month]:
                unemp_data_point = UnemploymentByStateMonthly(
                    state=state,
                    year=int(year),
                    month=month+1,
                    value=state_data[year][month]
                )
                unemp_data_point.save()

def insert_unemployment_all_states( data):
    for state in data.keys():
        insert_unemployment_state(state,data[state])

def main():
    path = '/home/menarguez/codes/natality'
    ext = 'xlsx'
    files = getFilesInDir(path,ext)
    print "Reading data"
    data = retrieve_data(path,files)
    print(data)
    # print(data)
    #print "inserting data to db"
    #insert_unemployment_all_states(data)

# if __name__ == "__main__":
main()
