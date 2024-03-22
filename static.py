
# ----------------------------------------------------------------------------
# FILE: static.py
#
# DESCRIPTION:
# This Python file contains all the data need to generate reports
#
# AUTHOR: Mohamad kassab
# DATE: Jan 19, 2024
# ----------------------------------------------------------------------------

# ----------------------------------------------------------------------------
# SECTION 1: Json objects
# ----------------------------------------------------------------------------

subscribers_json = [
    {
        "name": "Group 1",
        "emails": [
                "x@gmail.com",
                "y@gmail.com"
                ]
    },
    {
        "name": "Group 2",
        "emails": [
                "z@gmail.com"
                ] 
    }
]

queries_json = [
    {
        "id": "1",
        "syntax": """

           Select * From testTable1 


        """
    },

    {
        "id": "2",
        "syntax": """ 

        SELECT TOP (1000000) * FROM testTable2
        where country = 'lebanon'

        """
    }
]

databases_json=[
    {
        "enable": "true",
        "database_name": "yourdbname",
        "reports":[

            {
                "enable": "true",
                "queryId": "1",
                "subscribers": ["Group 1"],
                "report_name": "choose your report name",
                "saving_path":r".\Reports",
                "formats": ["xlsx"],
                "timing": {
                    "enable": "false",
                    "day": ["monday", "thursday"],
                    "hour": ["8:00"]
                } 
            },

            {
                "enable": "false",
                "queryId": "2", 
                "subscribers": ["Group 2"],
                "report_name": "test",
                "formats": ["xlsx"],
                "saving_path":r".\Reports",
                "timing": {
                    "enable": "false",
                    "day": ["monday", "thursday"],
                    "hour": ["8:00"]
                }
            }
        ]      
    }
]

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------