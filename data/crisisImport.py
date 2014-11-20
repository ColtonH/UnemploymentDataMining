# Author: John Johnson
from openpyxl import load_workbook
from openpyxl.cell import get_column_letter
import os
from data.models import Crisis

years = ['2008','2009','2010','1986','1987','1988','1989']

for y in years:
    try:
        c = Crisis.objects.get(year=y)
    except Exception, e:
        c = Crisis(year=y)
        try:
            c.save()
        except Exception, e:
            print "Error adding crisis for "+y
            print "Exit..."
            sys.exit(0)
