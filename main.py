# ----------------------------------------------------------------------------
# FILE: main.py
#
# DESCRIPTION:
# This Python file is the entry point of this automation software, it is from where we implement the logic.
#
# AUTHOR: Mohamad kassab
# DATE: Jan 18, 2024
# ----------------------------------------------------------------------------

# Import necessary libraries/modules
from database import Database
from helper import Helper
from formatting import Formatting
from emailService import Email
from static import databases_json, subscribers_json, queries_json
import os
import win32com.client as win32

# ----------------------------------------------------------------------------
# SECTION 1: Functions
# ----------------------------------------------------------------------------

def report_request(receiver, reports_name):
    helper = Helper()
    if receiver and reports_name:
        for report_name in reports_name:
           reportId =  helper.get_key_value(databases_json,["reports"], "report_name", report_name)
           print(reportId["subscribers"])
    else:
        return None


def report_generator():
    """
    This function will excute specific queries in a each database,
    then it will take those data and put them inside specified documents,
    then it will send these documents to the specified audience

    Returns:
        None

    """
    try:
        formating = Formatting()
        helper = Helper()
        logger = helper.Logger()
        for database in databases_json:
            if database["enable"] == "true": 
                    with Database(database["database_name"]) as db:
                        db.connect()
                        logger.info("connected to datbase")                          
                        reports = database["reports"]
                        for report in reports:
                            if(report["enable"] == "true"):
                                timing =report["timing"]
                                if(timing["enable"] == "true"):
                                    logger.info(f"checking timing for report: {report["report_name"]}")
                                    isTime = helper.time_checking(timing["day"], timing["hour"])
                                    if isTime:
                                        logger.info(f"getting data from sql for report: {report.get("report_name")}")                                
                                        data, headers = db.excute_query(report["queryId"]) 
                                        if data:
                                            logger.info(f"generating formats for report: {report["report_name"]}")                                
                                            generated_data = formating.format(report, data, headers)
                                            if generated_data:
                                                emailService = Email()  
                                                logger.info(f"Sending by email report: {report["report_name"]}")     
                                                emailService.send(generated_data, report["subscribers"], subscribers_json) 
                                    else:
                                        logger.info(f"it is not the time for report: {report["report_name"]}")   
                                else:
                                    logger.info(f"getting data from sql for report: {report["report_name"]}")                                
                                    data, headers = db.excute_query(report["queryId"])
                                    if data:
                                        logger.info(f"generating formats for report: {report["report_name"]}")                                
                                        formating.format(report, data, headers)
                                        generated_data = formating.format(report, data, headers)
                                        if generated_data:
                                            emailService = Email()  
                                            logger.info(f"Sending by email report: {report["report_name"]}")     
                                            emailService.send(generated_data, report["subscribers"], subscribers_json) 
                                                                            
    except Exception as e:
        logger.error("%s", e, exc_info=True)  

# ----------------------------------------------------------------------------
# SECTION 2: Entry point
# ----------------------------------------------------------------------------

if __name__ == "__main__":
    try:
        report_generator()
        
    except Exception as e:
        helper = Helper()
        logger = helper.Logger()
        logger.error("%s", e, exc_info=True)  

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------