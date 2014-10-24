import getopt
import gspread
import logging
import json
import sys

from oauth2client.client import SignedJwtAssertionCredentials


def usage():
  print "Usage: -u <username> -p <password> -k <key-file> -s <sheet-key>"
  
def main(argv):
  
  key_file = None
  username = None
  password = None
  sheet_key = None
  data = {}
  
  try:
    opts, args = getopt.getopt(argv, "hu:p:k:s:", ["help", "user=", "password=", "key=", "sheet="])
  except getopt.GetoptError:
    usage()
    sys.exit(2)
  
  for opt, arg in opts:
    if opt in ("-h", "--help"):
      usage()
      sys.exit()
    elif opt in ("-k", "--key"):
      key_file = arg
    elif opt in ("-u", "--user"):
      username = arg
    elif opt in ("-p", "--password"):
      password = arg
    elif opt in ("-s", "--sheet"):
      sheet_key = arg
  
  if (username == None and (key_file == None or password == None)) or sheet_key == None:
    usage()
    sys.exit(2)
  
  if key_file:
    
    try:
    
      f = file(key_file, 'rb')
      key = f.read()
      f.close()
      
      scope = ['https://spreadsheets.google.com/feeds', 'https://docs.google.com/feeds']
      credentials = SignedJwtAssertionCredentials(username, key, scope)
      gc = gspread.authorize(credentials)
      
    except Exception as e:
      print e.message
      sys.exit(1)
      
  elif username and password:
    gc = gspread.login(username, password)
  
  try:
    sheet = gc.open_by_key(sheet_key)
  except gspread.exceptions.SpreadsheetNotFound:
    print "Unable to find spreadsheet \"%s\" -- unable to continue." % sheet_key
    sys.exit(1)
  
  worksheets = sheet.worksheets()

  for worksheet in worksheets:
    data[worksheet.title] = worksheet.get_all_records()
  
  print json.dumps(data, indent=2)

if __name__ == "__main__":
  
  main(sys.argv[1:])