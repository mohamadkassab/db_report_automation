# ----------------------------------------------------------------------------
# FILE: helpers.py
#
# DESCRIPTION:
# This Python file will contain functions for different purposes to help us
#
# AUTHOR: Mohamad kassab
# DATE: Jan 18, 2024
# ----------------------------------------------------------------------------

# Import necessary libraries/modules
from datetime import datetime, timedelta
from static import queries_json, subscribers_json
import logging
import os
# ----------------------------------------------------------------------------
# SECTION 1: Helpers class
# ----------------------------------------------------------------------------

class Helper:
    
    def __init__(self):
        self.queries = queries_json
        self.subscribers = subscribers_json
        self.log_path = r".\logs\\"

    def time_checking(self, days, hours):
        """
        This function will check if the given time meets our condition
        if at least one day at any hour meets the requirements then the
        function will retrun True.

        Args:
            days: a list that contains the permitted days 
            hours: a list that contains the permitted hours 

        Returns:
            Bool

        """
        try:
            for day in days:
                current_date = datetime.now()
                current_day = current_date.strftime("%A").lower()
                if current_day == day:
                    for time in hours:
                        target_time = datetime.strptime(time, "%H:%M")                    
                        start_time = current_date - timedelta(minutes=5)
                        end_time = current_date + timedelta(minutes=5)
                        target_minutes = target_time.hour * 60 + target_time.minute
                        start_minutes = start_time.hour * 60 + start_time.minute
                        end_minutes = end_time.hour * 60 + end_time.minute
                        if start_minutes <= target_minutes <= end_minutes:
                            return True
            return False
        except Exception as e:
              self.logger.error("%s", e, exc_info=True)     
              return False
        
    def get_report_attribute(self, objects, key, value):
        """
        This function will get the syntax of a query based
        on its Id from static.py

        Args:
            queryId: The Id of the query
           
        Returns:
            string: the syntax query

        """
    
        try:
            for object in objects:    
                  if object[key] == value:
                      return object
            return None
        
        except Exception as e:
            self.logger.error("%s", e, exc_info=True)     
            return None
 
    def authenticate_receiver(self, receiverGroup, receiverEmail):
        """
        This function will authenticate if the receiver have
        access to the report.

        Args:
            receiver: the email address of the receiver
           
        Returns:
            bool

        """
    
        try:
            logger = self.Logger()
            for subscriptionGroup in self.subscribers:
                if subscriptionGroup["name"] == receiverGroup:
                    for email in subscriptionGroup["emails"]:
                        if email == receiverEmail:
                            return True
                    return False
        except Exception as e:
            logger.error("%s", e, exc_info=True)     
            return False
        
    def Logger(self):
        """
        This function will return a logger so we can save all the logs
            
        Returns:
            logger: logger handler

        """
               
        try:
            now = datetime.now()
            logger = logging.getLogger('ProvisioningPython')

            # Configure file handler
            if not len(logger.handlers):
                logger.setLevel(logging.DEBUG)
                if not os.path.exists(self.log_path):
                    os.makedirs(self.log_path)
                
                file_handler = logging.FileHandler(self.log_path + now.strftime("%Y-%m-%d") + '.log')
                formatter = logging.Formatter('------------------------------\n%(asctime)s ===> %(levelname)s\n %(message)s')
                file_handler.setFormatter(formatter)
                logger.addHandler(file_handler)

                # Configure console (stream) handler
                console_handler = logging.StreamHandler()
                console_handler.setFormatter(formatter)
                logger.addHandler(console_handler)

            return logger

        except Exception as e:
            logger.error("%s", e, exc_info=True)     
            return None
       
# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
