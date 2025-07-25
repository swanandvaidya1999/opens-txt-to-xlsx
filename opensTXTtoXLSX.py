#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import streamlit as st
import os

st.title("Convert Coded-opens TXT File to Excel")

# File uploader
uploaded_file = st.file_uploader("Upload your .txt file", type="txt")

if uploaded_file is not None:
    # Read lines
    lines = uploaded_file.read().decode("utf-8").splitlines()

    # Parse data
    data = []
    for line in lines:
        if line.strip().startswith("|") and not line.strip().startswith("|---"):
            parts = line.strip().split("|")
            if len(parts) >= 4:
                respid = parts[1].strip()
                response = parts[2].strip()
                codes = parts[3].strip().split(",")
                data.append([respid, response] + codes)

    # Determine max number of code columns
    max_codes = max(len(row) - 2 for row in data)
    columns = ["respid", "response"] + [f"code_{i+1}" for i in range(max_codes)]

    # Pad rows
    for row in data:
        while len(row) < len(columns):
            row.append("")

    # Create DataFrame
    df = pd.DataFrame(data, columns=columns)

    # Prepare output filename
    base_name = os.path.splitext(uploaded_file.name)[0]
    output_file = f"{base_name}.xlsx"

    # Save to Excel
    df.to_excel(output_file, index=False)

    # Download button
    with open(output_file, "rb") as f:
        st.download_button("📥 Download Excel File", f, file_name=output_file, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    st.success(f"✅ File processed! Output saved as: {output_file}")


# In[ ]:




