# ----------------------------------------------------------------------------
# FILE: database.py
#
# DESCRIPTION:
# This Python file is responsible to take all actions related to the database connectivity.
#
# AUTHOR: Mohamad kassab
# DATE: Jan 18, 2024
# ----------------------------------------------------------------------------

# Import necessary libraries/modules
import pyodbc
import configparser
from static import queries_json
from helper import Helper

# ----------------------------------------------------------------------------
# SECTION 1: Database class
# ----------------------------------------------------------------------------

class Database:
    
    def __init__(self, database):
        self.helper = Helper()
        self.logger = self.helper.Logger()
        config = configparser.ConfigParser()
        config.read("config.ini")
        parameters = config[database]
        database = database
        server = parameters.get("server")
        username = parameters.get("username")
        password = parameters.get("password")
        driver = parameters.get("driver")
        self.connection_string = (
        r'DRIVER={};SERVER={};DATABASE={};ID={};PASSWORD={};Trusted_Connection=yes;'
        .format(driver, server, database, username, password)
        )
        self.connection = None
        self.cursor = None

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.close_connection()
        if exc_type is not None:
            print(f"Exception Type: {exc_type}")
            print(f"Exception Value: {exc_value}")
            print(f"Traceback: {traceback}")
        return False

    def connect(self):
        """
        This function will connect to a database
        
        Returns:
            None

        """
        try:        
            self.connection = pyodbc.connect(self.connection_string)
            self.cursor = self.connection.cursor()
        except Exception as e:
            self.logger.error("%s", e, exc_info=True)  

    def close_connection(self):
        """
        This function will close the connection to the database
        
        Returns:
            None

        """
        try:
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()
        except Exception as e:
            self.logger.error("%s", e, exc_info=True)  

    def excute_query(self, queryId):
        """
        This function will execute a query inside a database
        
        Returns:
            data: list of the fetched rows from the database
            headers: list of the related headers of the data list
            
        """
        try:
            query = self.helper.get_report_attribute(queries_json, "id", queryId)
            if query: 
                query_syntax = query["syntax"]
                self.cursor.execute(str(query_syntax))
                headers = [desc[0] for desc in self.cursor.description]
                data = self.cursor.fetchall()
                if data:
                    return data, headers
                else:
                    return None
            return None
        except Exception as e:
            self.logger.error("%s", e, exc_info=True)  
            
# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
