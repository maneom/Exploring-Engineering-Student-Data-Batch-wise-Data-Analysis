import preprocessor
import numpy as np
import pandas as pd
import streamlit as st
import csv
import os
import time

import plotly.express as px
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import cufflinks as cf
import seaborn as sns
import matplotlib.pyplot as plt

init_notebook_mode(connected=True)
cf.go_offline()

def dataAnalysis(df):

    analysis_type = st.sidebar.selectbox('EXPLORATORY DATA ANLYSIS', ['ACADEMIC PERFORMANCE SUMMARY','GRAPHICAL INSIGHTS'])
    columns = selected_batch.columns

    if analysis_type == 'ACADEMIC PERFORMANCE SUMMARY':
        if "FE STATUS" in columns:
            st.markdown(
                f'<br><br><div style="text-align: center;background-color:#D0F6DE;"><h3><u>Academic Performance Summary of FE Students<u></h3></div>',
                unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            col1.write("NUMBER OF STUDENT APPEARED : " + str(df[df['TYPE'] == 'REGULAR'].shape[0]))
            col2.write("NUMBER OF STUDENT CLEARED ALL SUBJECT : " + str(
                df[((df['TYPE'] == 'REGULAR') & ((df['FE STATUS'] != 'ATKT') & (df['FE STATUS'] != 'FAIL')))].shape[0]))
            col1.write("NUMBER OF STUDENT WITH ATKT : " + str(
                df[((df['TYPE'] == 'REGULAR') & (df['FE STATUS'] == 'ATKT'))].shape[0]))
            col2.write("NUMBER OF STUDENT GOT YEAR DOWN : " + str(
                df[((df['TYPE'] == 'REGULAR') & (df['FE STATUS'] == 'FAIL'))].shape[0]))
            st.warning("TOTAL STUDENT MOVED TO NEXT YEAR : " + str(
                df[((df['TYPE'] == 'REGULAR') & (df['FE STATUS'] != 'FAIL'))].shape[0]))

        for col in ['SE STATUS', 'TE STATUS']:
            if col in columns:
                # TYPE = REGULAR
                st.markdown(
                    f'<br><br><div style="text-align: center;background-color:#D0F6DE;"><h3><u>Academic Performance Summary of {col.split()[0]} Students<u></h3></div>',
                    unsafe_allow_html=True)
                st.markdown(f'<div style=";"><h5>REGULAR STUDENTS DATA</h5></div>', unsafe_allow_html=True)
                col1, col2 = st.columns(2)
                col1.write("NUMBER OF STUDENT APPEARED : " + str(df[df['TYPE'] == 'REGULAR'].shape[0]))
                col2.write("NUMBER OF STUDENT CLEARED ALL SUBJECT : " + str(
                    df[((df['TYPE'] == 'REGULAR') & ((df[col] != 'ATKT') & (df[col] != 'FAIL')))].shape[0]))
                col1.write("NUMBER OF STUDENT WITH ATKT : " + str(
                    df[((df['TYPE'] == 'REGULAR') & (df[col] == 'ATKT'))].shape[0]))
                col2.write("NUMBER OF STUDENT GOT YEAR DOWN : " + str(
                    df[((df['TYPE'] == 'REGULAR') & (df[col] == 'FAIL'))].shape[0]))
                st.warning("TOTAL STUDENT MOVED TO NEXT YEAR : " + str(
                    df[((df['TYPE'] == 'REGULAR') & (df[col] != 'FAIL'))].shape[0]))
                # TYPE = DSE/ Branch Transfer/ OTHER
                st.markdown(f'<div style=";"><h5>DSE, BRANCH TRANSFERRED STUDENTS DATA</h5></div>',
                            unsafe_allow_html=True)
                col1, col2 = st.columns(2)
                col1.write("NUMBER OF STUDENT APPEARED : " + str(df[df['TYPE'] != 'REGULAR'].shape[0]))
                col2.write("NUMBER OF STUDENT CLEARED ALL SUBJECT : " + str(
                    df[((df['TYPE'] != 'REGULAR') & ((df[col] != 'ATKT') & (df[col] != 'FAIL')))].shape[0]))
                col1.write("NUMBER OF STUDENT WITH ATKT : " + str(
                    df[((df['TYPE'] != 'REGULAR') & (df[col] == 'ATKT'))].shape[0]))
                col2.write("NUMBER OF STUDENT GOT YEAR DOWN : " + str(
                    df[((df['TYPE'] != 'REGULAR') & (df[col] == 'FAIL'))].shape[0]))
                st.warning("TOTAL STUDENT MOVED TO NEXT YEAR : " + str(
                    df[((df['TYPE'] != 'REGULAR') & (df[col] != 'FAIL'))].shape[0]))

        if 'BE STATUS' in columns:
            # TYPE = REGULAR
            st.markdown(
                f'<br><br><div style="text-align: center; background-color:#D0F6DE;"><h3><u>Academic Performance Summary of BE Students<u></h3></div>',
                unsafe_allow_html=True)
            st.markdown(f'<div style=";"><h5>REGULAR STUDENTS DATA</h5></div>', unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            col1.write("NUMBER OF STUDENT APPEARED : " + str(df[df['TYPE'] == 'REGULAR'].shape[0]))
            col2.write("NUMBER OF STUDENT CLEARED ALL SUBJECT : " + str(
                df[((df['TYPE'] == 'REGULAR') & (df['BE STATUS'] != 'RRB/FAIL'))].shape[0]))
            col1.write("NUMBER OF STUDENT GOT YEAR DOWN : " + str(
                df[((df['TYPE'] == 'REGULAR') & (df['BE STATUS'] == 'RRB/FAIL'))].shape[0]))
            st.warning("TOTAL STUDENT PASSED OUT : " + str(
                df[((df['TYPE'] == 'REGULAR') & ((df['BE STATUS'] != 'RRB/FAIL') & (df['BE STATUS'] != 'FAIL')))].shape[0]))
            # TYPE = DSE/ Branch Transfer/ OTHER
            st.markdown(f'<div style=";"><h5>DSE, BRANCH TRANSFERRED STUDENTS DATA</h5></div>', unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            col1.write("NUMBER OF STUDENT APPEARED : " + str(df[df['TYPE'] != 'REGULAR'].shape[0]))
            col2.write("NUMBER OF STUDENT CLEARED ALL SUBJECT : " + str(
                df[((df['TYPE'] != 'REGULAR') & (df['BE STATUS'] != 'RRB/FAIL'))].shape[0]))
            col1.write("NUMBER OF STUDENT GOT YEAR DOWN : " + str(
                df[((df['TYPE'] != 'REGULAR') & (df['BE STATUS'] == 'RRB/FAIL'))].shape[0]))
            st.warning("TOTAL STUDENT PASSED OUT : " + str(
                df[((df['TYPE'] != 'REGULAR') & (df['BE STATUS'] != 'RRB/FAIL'))].shape[0]))

            summary = pd.DataFrame(
                columns=['YEAR', 'TYPE', 'NO. OF STUDENTS APPEARED', 'NO. OF STUDENTS CLEARED ALL SUBJECT',
                         'NO. OF STUDENTS GOT ATKT', 'NO. OF STUDENTS GOT YEAR DOWN',
                         'NO> OF STUDENTS MOVED TO NEXT YEAR'])
            summary = pd.concat((summary, pd.DataFrame([["FE",
                                                         "REGULAR",
                                                         str(df[df['TYPE'] == 'REGULAR'].shape[0]),
                                                         str(df[((df['TYPE'] == 'REGULAR') & (
                                                                     (df['FE STATUS'] != 'ATKT') & (
                                                                     df['FE STATUS'] != 'FAIL')))].shape[0]),
                                                         str(df[((df['TYPE'] == 'REGULAR') & (
                                                                     df['FE STATUS'] == 'ATKT'))].shape[0]),
                                                         str(df[((df['TYPE'] == 'REGULAR') & (
                                                                 df['FE STATUS'] == 'FAIL'))].shape[0]),
                                                         str(df[((df['TYPE'] == 'REGULAR') & (
                                                                 df['FE STATUS'] != 'FAIL'))].shape[0])
                                                         ]], columns=summary.columns)))
            for col in ['SE STATUS', 'TE STATUS']:
                summary = pd.concat((summary, pd.DataFrame([[col.split()[0],
                                                             "REGULAR",
                                                             str(
                                                                 df[df['TYPE'] == 'REGULAR'].shape[0]),
                                                             str(
                                                                 df[((df['TYPE'] == 'REGULAR') & (
                                                                             (df[col] != 'ATKT') & (
                                                                                 df[col] != 'FAIL')))].shape[0]),
                                                             str(
                                                                 df[((df['TYPE'] == 'REGULAR') & (
                                                                             df[col] == 'ATKT'))].shape[0]),
                                                             str(
                                                                 df[((df['TYPE'] != 'REGULAR') & (
                                                                             df[col] == 'FAIL'))].shape[0]),
                                                             str
                                                             (df[((df['TYPE'] == 'REGULAR') & (
                                                                         df[col] != 'FAIL'))].shape[0])
                                                             ]], columns=summary.columns)))
                summary = pd.concat((summary, pd.DataFrame([[col.split()[0],
                                                             "DSE/BRANCH TRANSFER",
                                                             str(
                                                                 df[df['TYPE'] != 'REGULAR'].shape[0]),
                                                             str(
                                                                 df[((df['TYPE'] != 'REGULAR') & (
                                                                             (df[col] != 'ATKT') & (
                                                                                 df[col] != 'FAIL')))].shape[0]),
                                                             str(
                                                                 df[((df['TYPE'] != 'REGULAR') & (
                                                                             df[col] == 'ATKT'))].shape[0]),
                                                             str(
                                                                 df[((df['TYPE'] != 'REGULAR') & (
                                                                             df[col] == 'FAIL'))].shape[0]),
                                                             str(
                                                                 df[((df['TYPE'] != 'REGULAR') & (
                                                                             df[col] != 'FAIL'))].shape[0])
                                                             ]], columns=summary.columns)))
            col = "BE STATUS"
            summary = pd.concat((summary, pd.DataFrame([[col.split()[0],
                                                         "REGULAR",
                                                         str(
                                                             df[df['TYPE'] == 'REGULAR'].shape[0]),
                                                         str(
                                                             df[((df['TYPE'] == 'REGULAR') & (
                                                                         df[col] != 'FAIL'))].shape[0]),
                                                         str(
                                                             df[((df['TYPE'] == 'REGULAR') & (
                                                                         df[col] == 'ATKT'))].shape[0]),
                                                         str(
                                                             df[((df['TYPE'] != 'REGULAR') & (
                                                                     df[col] == 'FAIL'))].shape[0]),
                                                         str
                                                         (df[((df['TYPE'] == 'REGULAR') & (df[col] != 'FAIL'))].shape[
                                                              0])
                                                         ]], columns=summary.columns)))
            summary = pd.concat((summary, pd.DataFrame([[col.split()[0],
                                                         "DSE/BRANCH TRANSFER",
                                                         str(
                                                             df[df['TYPE'] != 'REGULAR'].shape[0]),
                                                         str(
                                                             df[((df['TYPE'] != 'REGULAR') & ((df[col] != 'ATKT') & (
                                                                         df[col] != 'FAIL')))].shape[0]),
                                                         str(
                                                             df[((df['TYPE'] != 'REGULAR') & (
                                                                         df[col] == 'ATKT'))].shape[0]),
                                                         str(
                                                             df[((df['TYPE'] != 'REGULAR') & (
                                                                         df[col] == 'FAIL'))].shape[0]),
                                                         str(
                                                             df[((df['TYPE'] != 'REGULAR') & (
                                                                         df[col] != 'FAIL'))].shape[0])

                                                         ]], columns=summary.columns)))
            summary.reset_index(drop=True, inplace=True)
            st.write(summary)

            st.error("IF SUMMARY IS INCORRECT. PLEASE MAKE CHANGES IN STATUS VALUES LIKE ATKT, FAIL.")
            if st.checkbox("DO YOU WANT TO DOWNLOAD SUMMARY TO FILE ?"):
                requestedFile = batch_name + "_summary" + ".csv"
                summary.to_csv(requestedFile)
                progress = st.progress(0)
                for i in range(100):
                    time.sleep(.01)
                    progress.progress(i + 1)
                st.success("FILE DOWNLOADED "+ requestedFile)

    elif analysis_type == 'GRAPHICAL INSIGHTS':
        availableSGPA = []
        if "BE SGPA" in df.columns:
            availableSGPA = ['FE SGPA', 'SE SGPA', 'TE SGPA', 'BE SGPA']
        elif "TE SGPA" in df.columns:
            availableSGPA = ['FE SGPA', 'SE SGPA', 'TE SGPA']
        elif "SE SGPA" in df.columns:
            availableSGPA = ['FE SGPA', 'SE SGPA']
        elif "FE SGPA" in df.columns:
            availableSGPA = ['FE SGPA']

        if len(availableSGPA) != 0:

            st.markdown('<br><hr><hr>',
                        unsafe_allow_html=True)
            prn = st.selectbox("ENTER STUDENTS PRN ", df['PRN'].values)
            if st.button("SUBMIT"):
                st.markdown('<div style="text-align: center;"><h4>STUDENT PERFORMANCE ANALYSIS</h4></div>',unsafe_allow_html=True)
                col1, col2, col3 = st.columns([1, 4, 1])
                data = df[df['PRN'] == prn][availableSGPA]
                data = data.astype(float)
                fig, ax = plt.subplots()
                plt.xticks(rotation="vertical")
                ax = sns.barplot(data)
                ax.set_ylim(1, 10)
                sns.set_style('darkgrid')
                col2.pyplot(fig)

            availableStatus = []
            if "BE STATUS" in df.columns:
                availableStatus = ['FE STATUS', 'SE STATUS', 'TE STATUS', 'BE STATUS']
            elif "TE STATUS" in df.columns:
                availableStatus = ['FE STATUS', 'SE STATUS', 'TE STATUS']
            elif "SE STATUS" in df.columns:
                availableStatus = ['FE STATUS', 'SE STATUS']
            elif "FE STATUS" in df.columns:
                availableStatus = ['FE STATUS']

            if len(availableStatus)>=1:
                st.markdown('<br><br><hr><div style="text-align: center;"><h4>YEAR WISE BATCH ANALYSIS</h4></div>',
                            unsafe_allow_html=True)
                col1, col2 = st.columns(2)
                i = 'FE STATUS'
                data = df[df['TYPE'] == 'REGULAR'][i].value_counts()
                cols = [j for j in df[df['TYPE'] == 'REGULAR'][i].unique()]
                fig, ax = plt.subplots()
                ax = plt.pie(data, labels=cols, autopct='%1.1f%%')
                plt.legend(title=i)
                col1.pyplot(fig)
            if len(availableStatus)>=2:
                i = 'SE STATUS'
                data = df[i].value_counts()
                cols = [j for j in df[i].unique()]
                fig, ax = plt.subplots()
                ax = plt.pie(data, labels=cols, autopct='%1.1f%%')
                plt.legend(title=i)
                col2.pyplot(fig)
            if len(availableStatus) >=3:
                i = 'TE STATUS'
                data = df[i].value_counts()
                cols = [j for j in df[i].unique()]
                fig, ax = plt.subplots()
                ax = plt.pie(data, labels=cols, autopct='%1.1f%%')
                plt.legend(title=i)
                col1.pyplot(fig)
            if len(availableStatus) == 4:
                i = 'BE STATUS'
                data = df[i].value_counts()
                cols = [j for j in df[i].unique()]
                fig, ax = plt.subplots()
                ax = plt.pie(data, labels=cols, autopct='%1.1f%%')
                plt.legend(title=i)
                col2.pyplot(fig)

            if len(availableSGPA) != 0:
                st.markdown('<br><br><hr><div style="text-align: center;"><h4>DISTRIBUTION OF SGPA</h4></div>',
                            unsafe_allow_html=True)
                col1, col2, col3 = st.columns([1, 4, 1])
                fig, ax = plt.subplots()
                ax = sns.boxplot(df[availableSGPA])
                col2.pyplot(fig)


# User menu for selecting options
st.set_page_config(layout="wide")
user_menu = st.sidebar.radio("Choose Options", ["HOME PAGE", "ALL BATCHES", "CREATE NEW BATCH"])

if user_menu == "HOME PAGE":
    image_path = "i2it_logo.png"
    col1,col2,col3 = st.columns([3,1,3])
    col2.image("i2it_logo.png",width=100)
    st.markdown('<div style="text-align: center;"><h2>INTERNATIONAL INSTITUTE OF INFORMATION TECHNOLOGY</h2><br></div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align: center;"><h6>Approved by AICTE | Recognized by DTE, Govt. of Maharashtra | Affiliated to the Savitribai Phule Pune University</h6></div>',unsafe_allow_html=True)
    st.markdown('<div style="text-align: center;"><h6> Accredited by NAAC | NBA Accredited - 2 UG Programmes</h6></div>',unsafe_allow_html=True)
    st.markdown('<div style="text-align: center;"><h6> Recognized u/s 2(f) of the UGC Act, 1956</h6></div>',unsafe_allow_html=True)
    st.markdown('<br><div style="text-align: center;"><h4><u> BATCH-WISE RESULT ANALYSIS</u></h4></div>',unsafe_allow_html=True)
# Creating a new batch
elif user_menu == "CREATE NEW BATCH":
    pdf = None
    flag = 0
    with st.form("NEW BATCH"):          # ,clear_on_submit=True chgs o/p
        batch_name = st.text_input("ENTER BATCH NAME")
        enter_students_detail = st.selectbox("FORM TO ENTER STUDENTS DETAILS",["SELECT", "ENTER MANUALLY", "UPLOAD FILE"])
        submitted = st.form_submit_button("SUBMIT")

        if submitted:
            # Write the new batch name to the CSV file
            batchList = pd.read_csv("batchList.csv")
            if str(batch_name) in batchList["Batch Name"].astype(str).tolist():
                print("ALREADY EXITS")
                flag = 1

            if enter_students_detail !="SELECT":
                pass
            else:
                st.error("PLEASE RECHECK DETAILS")
            if flag==0 and batch_name=="":
                flag=1
                st.error("PLEASE RECHECK DETAILS")

        if flag == 0:
            if enter_students_detail == "UPLOAD FILE":          # --> Uploading File
                pdf = st.file_uploader("UPLOAD A FILE")
                st.form_submit_button("SUBMIT FILE")
                if pdf:
                    try:
                        pdf_content = pdf.read()
                        studentList = preprocessor.convert_text_to_table(pdf_content)
                        b_name = batch_name + '.csv'
                        studentList.to_csv(b_name,index=False)
                        st.success("BATCH CREATED SUCCESFULLY")
                        with open('batchList.csv', 'a', newline='') as file:
                            writer = csv.writer(file)
                            writer.writerow([batch_name])
                    except Exception as e:
                        st.error("FILE NOT IN REQUIRED FORMAT")

            elif enter_students_detail == "ENTER MANUALLY":     # --> Inserting Value
                col1, col2 = st.columns(2)
                prn = col1.text_area("ENTER PRN NUMBER ")
                names = col2.text_area("ENTER NAME")
                if st.form_submit_button("SUBMIT DATA") :
                    df = pd.DataFrame(prn.split("\n"), columns=["PRN"])
                    df['Student Name'] = names.split("\n")
                    b_name = batch_name + '.csv'
                    df.to_csv(b_name, index=False)
                    st.success("BATCH CREATED SUCCESFULLY")
                    with open('batchList.csv', 'a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow([batch_name])
        elif flag == 1:
            st.error("BATCH ALREADY EXITS")

# Opening Batch
elif user_menu == "ALL BATCHES":
    # Read existing batches from the CSV file
    batchList = pd.read_csv("batchList.csv")

    # Check if there are existing batches
    if len(batchList['Batch Name'].tolist()) != 0:
        batch_name = st.selectbox("Choose Batch", ["SELECT"]+batchList['Batch Name'].tolist())
        add_yr_sgpa = False
        if batch_name == "SELECT":
            pass
        else:
            selected_batch = pd.read_csv(str(batch_name)+".csv")

            # ADDING DATA
            column_required = "no new col required"
            if "FE SGPA" not in selected_batch.columns.tolist():
                column_required = "FE SGPA"
            elif "FE STATUS" not in selected_batch.columns.tolist():
                column_required = "FE STATUS"
            elif "SE SGPA" not in selected_batch.columns.tolist():
                column_required = "SE SGPA"
            elif "SE STATUS" not in selected_batch.columns.tolist():
                column_required = "SE STATUS"
            elif "TE SGPA" not in selected_batch.columns.tolist():
                column_required = "TE SGPA"
            elif "TE STATUS" not in selected_batch.columns.tolist():
                column_required = "TE STATUS"
            elif "BE SGPA" not in selected_batch.columns.tolist():
                column_required = "BE SGPA"
            elif "BE STATUS" not in selected_batch.columns.tolist():
                column_required = "BE STATUS"

            if column_required != "no new col required":
                options = st.radio("SELECT OPERATION",["SHOW DATA", "ADD "+column_required, "EDIT", "DROP BATCH"])
            else:
                options = st.radio("SELECT OPERATION", ["SHOW DATA","EDIT", "DROP BATCH"])


            if options == "SHOW DATA":
                st.dataframe(selected_batch, width=1000)

                # ANALYSIS OF AVAILABLE YEARS

                dataAnalysis(selected_batch)

            elif options == "ADD "+column_required:
                with st.form("ADD DATA"):
                    sgpa_values = st.text_area("ADD " + column_required)
                    if st.form_submit_button("SUBMIT"):
                        if( len(sgpa_values.split("\n")) == selected_batch.shape[0]):
                            # TYPE AS REGULAR
                            if column_required == 'FE SGPA':
                                selected_batch["TYPE"] = "REGULAR"

                            # SAVING SGPA
                            selected_batch[column_required] = sgpa_values.split("\n")
                            selected_batch.to_csv(str(batch_name)+".csv", index=False)
                            st.success("NEW COLUMN ADDED")
                        else:
                            st.error("DATA IS INCONSISTENT!!!")

            elif options == "EDIT":
                option = st.selectbox("SELECT CHOISE", ["SELECT", "RENAME STUDENT", "DROP STUDENT", "ADD STUDENT"]+["UPDATE "+i for i in selected_batch.columns[3:].tolist()])
                if option == "DROP STUDENT":
                    with st.form("DROP STUDENT"):
                        prn = st.text_input("Enter student's PRN to be deleted")

                        if st.form_submit_button("SUBMIT") :
                            if selected_batch[selected_batch["PRN"]==prn].shape[0] == 1:        # HAS EXACTLY ONE ROW FOR SELECTED PRN
                                selected_batch.drop(selected_batch[selected_batch["PRN"] == prn].index[0], inplace=True)
                                selected_batch.reset_index(inplace=True)
                                selected_batch.drop(["index"], axis=1, inplace=True)
                                selected_batch.to_csv(str(batch_name)+".csv", index=False)
                                st.success("PRN DELETED")
                            else:
                                st.error("STUDENT NOT FOUND")
                elif option == "ADD STUDENT":
                    with st.form("ADD STUDENT"):
                        prn = st.text_input("ENTER PRN OF STUDENT")
                        name = st.text_input("ENTER NAME OF STUDENT")
                        type = st.radio('SELECT ADMISSION TYPE OF STUDENT',['DSE','BRANCH TRANSFER','REGULAR','OTHERS'])
                        if st.form_submit_button("ADD GIVEN STUDENT"):
                            if prn not in selected_batch["PRN"].tolist():
                                new_selected_batch = pd.concat((selected_batch, pd.DataFrame([[prn, name,type]], columns=["PRN", "Student Name", "TYPE"]))).sort_values("Student Name")
                                new_selected_batch.to_csv(str(batch_name)+".csv", index=False)
                                st.success("STUDENT ADDED")
                            else:
                                st.error("STUDENT ALREADY PRESENT")
                elif option in ["UPDATE "+i for i in selected_batch.columns[2:].tolist()]:
                    selected_year = " ".join(option.split()[1:])
                    st.write(selected_year)
                    with st.form("UPDATE MARKS"):
                        prn = st.text_input("Please enter the student PRN for which the data is to be changed.")
                        new_marks = st.text_input("ENTER NEW DATA")
                        if st.form_submit_button("SUBMIT DATA"):
                            if prn in selected_batch["PRN"].tolist():
                                selected_batch.loc[selected_batch["PRN"] == prn, selected_year] = new_marks
                                selected_batch.to_csv(str(batch_name)+".csv", index=False)
                                st.success("SUBMITTED")
                            else:
                                st.error("GIVEN PRN DON'T EXIT")
                elif option == "RENAME STUDENT":
                    with st.form("RENAME STUDENT"):
                        prn = st.text_input("Please enter the student PRN for which the name is to be changed.")
                        name = st.text_input("ENTER NEW NAME")
                        if st.form_submit_button("RENAME STUDENT"):
                            if prn in selected_batch["PRN"].tolist():
                                selected_batch.loc[selected_batch["PRN"] == prn, "Student Name"] = name
                                selected_batch.to_csv(str(batch_name) + ".csv", index=False)
                                st.success("SUBMITTED")
                            else:
                                st.error("GIVEN PRN DON'T EXIT")
            elif options =="DROP BATCH":
                st.warning("ONCE DELETED BATCH CAN'T BE RETRIEVED AGAIN !!!")
                if st.checkbox("CONFIRM TO DELETE FILE"):
                    progress = st.progress(0)
                    for i in range(100):
                        time.sleep(.01)
                        progress.progress(i+1)

                    batchList.drop(batchList[batchList["Batch Name"] == batch_name].index[0], inplace=True)
                    print(selected_batch)
                    batchList.reset_index(inplace=True)
                    batchList.drop(["index"], axis=1, inplace=True)
                    print(batchList)
                    batchList.to_csv("batchList.csv", index=False)

                    os.remove(str(batch_name)+".csv")

                    st.success("BATCH DROPPED")


    else:
        st.error("NO BATCH EXIT")