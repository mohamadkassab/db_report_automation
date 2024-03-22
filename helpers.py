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
from static import queries_dic

# ----------------------------------------------------------------------------
# SECTION 1: Helpers class
# ----------------------------------------------------------------------------

class Helpers:
    
    def __init__(self):
        self.queries = queries_dic

    def time_checking(days, hours):
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
              return False
        
    def get_query_by_id(self, queryId):
        for query in self.queries:
            if query.get("id") == queryId:
                return query.get("syntax")
        return None




            
# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
