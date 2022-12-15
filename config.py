file_name = "data"
extension = ".xlsx"
sheet_nm = "data"
# mask = ["Patient First Name",	"Patient Last Name",	"Patient Address",	"Patient City",	"Town",	"Patient Phone", "Patient Email_add1",	"Patient legal representative name"]
# roll_up = ["Patient DOB"]
# pat_zip = ["Patient Zip"]
mask = ["FirstName", "LastName", "PersonMobilePhone", "Phone", "PersonEmail",  "PxP_City__c "]
pat_zip = ["Postal_Code__c", "PxP_Postal_Code_other__c "]
translate_cols = ["Product id",	"Brand", "Indication", "Patient DOB", "Patient Prefecture",	"Patient County",	"Patient Gender ",  "Patient Preferred Language",	"Patient Preferred Method of Contact",	"Patient Best Time to Contact",	"Household_size",	"Adjusted_gross_income",	"Patient BMI",	"Patient Height",	"Patient Weight"]
salt = "ZS_PDM_JANSSEN"
hashed_cols = ["PersonBirthdate"]
restricted_zips = {
    '61': '61+71',
    '26': '26+27',
    '53': '53+54'
}
