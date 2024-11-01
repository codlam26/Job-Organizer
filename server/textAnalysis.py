#NLP_____________________________
#Check if any of the words matches with the "keyword"

#In the text identify the (Company Name) - (Job title)

#Dictionary of the Company Names with its status - (Offer , Progress, Rejected) and return that in a json
#eg. {'Google' : 'Sent', Amazon : 'In Progress'}

# def obtain_company_name

import re
import spacy

nlp = spacy.load("en_core_web_sm")

def get_organization_name(email_body):
    """Uses NLP to extract organization names from the email body."""
    doc = nlp(email_body)
    for ent in doc.ents:
        if ent.label_ == "ORG":
            return ent.text
    
    if "regret" in email_text.lower() or "not moving forward" in email_text.lower() or "unfortunately" in email_text.lower():
        return company_name, "Rejected"
    
    elif "Interview" in email_text.lower() and "schedule" in email_text.lower():
        return company_name, "Interview"
    
    elif "thank you for applying" in email_text.lower() or "thank you for your interest" in email_text.lower():
        return company_name, "Sent"

    return None

def get_sender_company(email_body):
    """Extract the company name through the text"""
    pattern = r"Thanks for applying to ([A-Za-z0-9\s&'\-]+)"
    # pattern = (r"Thank you for (?:applying to|your interest in) ([A-Za-z0-9\s&'\-]+)")
    apply_pattern = (
        r"Thank you for (?:applying to|your interest in|expressing interest in) ([A-Za-z0-9\s&'\-]+)"
    )

    reject_pattern = (
        r"(?:we regret to inform you|we are not interested in your application|"
        r"we will not be moving forward with your application|unfortunately, we cannot offer)"
        r" at ([A-Za-z0-9\s&'\-]+)"
    )

    match = re.search(pattern, email_body)
    if match:
        return match.group(1).capitalize()
    return None


