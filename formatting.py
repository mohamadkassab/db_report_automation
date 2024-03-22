# ----------------------------------------------------------------------------
# FILE: formatting.py
#
# DESCRIPTION:
# This Python file will contain functions to format our data to any other format
#
# AUTHOR: Mohamad kassab
# DATE: Jan 18, 2024
# ----------------------------------------------------------------------------

# Import necessary libraries/modules
import configparser
import numpy as np
import pandas as pd
from datetime import datetime
import os
from helper import Helper

# ----------------------------------------------------------------------------
# SECTION 1: Formatting Class
# ----------------------------------------------------------------------------

class Formatting:

    def __init__(self):
        self.helper = Helper()
        self.logger = self.helper.Logger()

    def xlsx_format(self, data, headers, report):
        """
        This function will convert any data to xlsx format
        and then save it in a specific path

        Args:
            data: list of data to treat
            headers: headers of the columns in data list
            report_name: the name of the report

        Returns:
            the path of generated file 

        """
        try:
            data = np.array(data)
            df = pd.DataFrame(data, columns=headers)
            current_datetime = datetime.now()
            year =  current_datetime.year
            month = current_datetime.month
            day = current_datetime.day
            file_path = r"{}\{}\{}_{}_{}_{}.xlsx".format(report["saving_path"],report["report_name"], report["report_name"], year, month, day)
            directory = os.path.dirname(file_path)
            if not os.path.exists(directory):
                os.makedirs(directory)
            df.to_excel(file_path, index=False)
            return file_path

        except Exception as e:
            self.logger.error("%s", e, exc_info=True)     
    
    def xml_format(self, data, headers, report_name):
        return ""

    def format(self, report, data, headers):
        """
        This function will iterate of the formats we want
        to covert our data and then call the necessary
        functions

        Args:
            query: it contains information related to the query
            data: list of data we want to iterate over
            headers: headers of the columns in data list

        Returns:
            list() of path of generated files 

        """
        if data:
            generated_reports = []
            switch_dict = {
                    'xlsx': self.xlsx_format,
                    'xml': self.xml_format
                }
            for format in report["formats"]:
                try:
                    handler = switch_dict.get(format, lambda: print("unknown format"))
                    file_path = handler(data, headers, report)
                    if file_path:
                        generated_reports.append(file_path)

                except Exception as e:
                     self.logger.error("%s", e, exc_info=True) 
                
            return generated_reports
        
        else:
            return None
                        

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
