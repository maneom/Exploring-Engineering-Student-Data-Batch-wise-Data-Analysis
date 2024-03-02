import PyPDF2
import pandas as pd
import io  # Add this line to import the 'io' module
def extract_tables_from_pdf(file):
    tables = []
    reader = PyPDF2.PdfReader(file)             # Directly file is passed
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        text = page.extract_text()
        # Identify and extract tables from the text
        # You may need to implement a more sophisticated table detection algorithm here
        tables.append(text)  # For demonstration purposes, just appending the entire text of each page

    return tables

def convert_text_to_table(pdf):   # As directly file is passed so it don't require to use open method so need explicitly to convert it into BytesIo
    pdf_stream = io.BytesIO(pdf)  # Wrap the bytes object in a BytesIO object
    tables = extract_tables_from_pdf(pdf_stream)

    seat_no = []
    name = []
    mother_name = []
    prn = []

    for table in tables:
        data = table.split("\n")
        headers = ['SeatNo', 'Student Name', 'Mother', 'PRN ']
        header_indices = [data.index(header) for header in headers]
        j = header_indices[3] + 1
        flag = 0
        while j < len(data):
            for i in ['Savitribai', 'Phule', 'Pune', 'University', " page ", "Page"]:
                if i in data[j]:
                    flag = 1
            if (flag == 1):
                break
            seat_no.append(data[j])
            j = j + 1
            name.append(data[j])
            j = j + 1
            mothername = []
            while ():
                mothername.append(data[j])
                j = j + 1
            while ((data[j].isalpha()) or (((not (data[j]).isalnum())) and (" " in data[j]))):
                mothername.append(data[j])
                j = j + 1
            mother_name.append(" ".join(mothername))
            prn.append(data[j])
            j = j + 1

    studentList = pd.DataFrame(prn, columns=['PRN'])
    studentList['Student Name'] = name

    return studentList
