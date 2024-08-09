import vobject
import csv

def vcard_to_csv(vcard_file, csv_file):
    # Open the vCard file with the correct encoding
    with open(vcard_file, 'r', encoding='utf-8') as f:
        vcard_data = f.read()

    # Parse the vCard data
    vcards = vobject.readComponents(vcard_data)

    # Open the CSV file for writing
    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Name', 'Email', 'Phone']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header row
        writer.writeheader()

        # Iterate over vCard objects
        for vcard in vcards:
            name = ''
            email = ''
            phone = ''

            # Extract name
            if 'fn' in vcard.contents:
                name = vcard.contents['fn'][0].value

            # Extract email
            if 'email' in vcard.contents:
                email = vcard.contents['email'][0].value

            # Extract phone number
            if 'tel' in vcard.contents:
                phone = vcard.contents['tel'][0].value

            # Write the contact to CSV
            writer.writerow({'Name': name, 'Email': email, 'Phone': phone})

if __name__ == "__main__":
    vcard_file = 'iCloud vCards.vcf'  # Input vCard file
    csv_file = 'contacts.csv'    # Output CSV file

    vcard_to_csv(vcard_file, csv_file)
    print(f"Contacts have been successfully written to {csv_file}")
