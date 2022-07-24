import streamlit as st
import pandas as pd
import os
from PIL import Image

st.markdown("<h1 style='text-align: center; color: white;'>CodinGrad</h1>", unsafe_allow_html=True)
def save_uploaded_file(uploadedfile):
  with open(os.path.join("Data",uploadedfile.name),"wb") as f:
     f.write(uploadedfile.getbuffer())
  return st.success("Saved file :{} in tempDir".format(uploadedfile.name))

st.title("Upload DEMO Register Data")
datafile = st.file_uploader("Register CSV", type=['csv'])
if datafile is not None:
    file_details = {"FileName":datafile.name,"FileType":datafile.type}
    df  = pd.read_csv(datafile, encoding = 'ISO-8859-1')
    st.dataframe(df)
    # Apply Function here
    save_uploaded_file(datafile)

st.title("Upload Course Paid CSV")
datafile = st.file_uploader("Paid CSV", type=['csv'])
if datafile is not None:
    file_details = {"FileName":datafile.name,"FileType":datafile.type}
    df  = pd.read_csv(datafile, encoding = 'ISO-8859-1')
    st.dataframe(df)
    # Apply Function here
    save_uploaded_file(datafile)


class difference_dataframe:
    
    def __init__(self, registereddata, paiddata):
        self.registereddata = pd.read_csv(registereddata, encoding = 'ISO-8859-1')
        self.paiddata = pd.read_csv(paiddata)

        self.registereddata = self.registereddata.rename(columns={"EMAIL":"Email"})
        
    def calls_data(self):
        call_data = self.registereddata[~self.registereddata['Email'].isin(self.paiddata['Email'])].reset_index().drop(['index'], axis=1)
        return call_data

@st.cache
def convert_df(df):
    return df.to_csv().encode('utf-8')

# print(os.path.join(os.getcwd(), "Data", "RegisterData.csv"))
result = st.button("Run")
if result:
    data_diff = difference_dataframe(
        registereddata=os.path.join(os.getcwd(), "Data", "testing_registrations.csv"),
        paiddata=os.path.join(os.getcwd(), "Data", "tetsingpaid.csv")
    ).calls_data()
    st.dataframe(data_diff)
    # data_diff.to_csv("./Data/CallsData.csv")
    csv = convert_df(data_diff)
    st.download_button(
        "Press to Download",
        csv,
        "CallsData.csv",
        "text/csv"
    )
else:
    pass

result_c = st.button("Clean Folder")
if result_c:
    os.remove("./Data/RegisterData.csv")
    os.remove("./Data/PaidData.csv")
    st.success("Files are Deleted")