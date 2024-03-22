# ----------------------------------------------------------------------------
# FILE: emailService.py
#
# DESCRIPTION:
# This Python file is responsible to provide email services.
#
# AUTHOR: Mohamad kassab
# DATE: Jan 19, 2024
# ----------------------------------------------------------------------------

# Import necessary libraries/modules
from email.message import EmailMessage
import configparser
import os 
from email.mime.application import MIMEApplication
from helper import Helper
import win32com.client

# ----------------------------------------------------------------------------
# SECTION 1: Email class
# ----------------------------------------------------------------------------

class Email:
     
    def __init__(self):
        self.helper = Helper()
        self.logger = self.helper.Logger()
        config = configparser.ConfigParser()
        config.read("config.ini")
        parameters = config["win32"]
        self.outlook = win32com.client.Dispatch("Outlook.Application")
        self.outlookService = self.outlook.GetNameSpace('MAPI')


    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.smtp.quit()
        if exc_type is not None:
            print(f"Exception Type: {exc_type}")
            print(f"Exception Value: {exc_value}")
            print(f"Traceback: {traceback}")
        return False
     
    def send(self, reports, receivers, subscribersGroups):
        """
        This function will send an email with an attached file
        
        Args:
            subscribers: list of subscribers we want to send them this email
            generated_reports: the path of generated reports we want to attach
            subscribersGroups: the list of all subscribers

        Returns:
            None

        """
        try:  
            if receivers:         
                for receiver in receivers:
                    for subscriberGroup in subscribersGroups:
                            if subscriberGroup["name"] == receiver:
                                emails = subscriberGroup["emails"]
                                for email in emails:
                                        mail = self.outlook.CreateItem(0)
                                        for report in reports:  
                                            file_name, file_extension = os.path.splitext(os.path.basename(report))                    
                                            file_path = os.path.join(os.path.dirname(report), file_name + file_extension)  
                                            mail.Attachments.Add(os.path.join(os.getcwd(), file_path))
                                       
                                        first_name, last_name = email.split("@")[0].split(".")
                                        mail.To = email
                                        mail.Subject = f"Automated report: {file_name}"   
                                        mail.BodyFormat = 1                                     
                                        mail.Body = f"Dear {first_name} {last_name}, \n\n Please find attached the report {file_name}.\n This report has been automatically generated and sent to you via email.\n\n Best regards, \n\n Mohamad kassab" 
                                        mail.Display()
                                        mail.Save()
                                        mail.Send()                                                 
                                break
        except Exception as e:
            self.logger.error("%s", e, exc_info=True)                                                           
                                
# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------